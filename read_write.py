##使用库设置
import linecache;
import numpy as np;
import os;
import sys;
import random
from itertools import combinations;
import math;
import copy


def VASPread(FileName):
    ##########读取VASP文件内的数据#############
    while os.path.exists(FileName) == False:
        if FileName == '0':
            sys.exit(0)
        print("VAPS结构文件未找到!! 若要退出请输入数字0")
        FileName = input("重新输入VAPS结构文件名: ")
    else:
        File0aj = open(FileName)  # 打开结构文件
    try:
        key = linecache.getline(FileName, 8).split()[0]
        if key == "Direct" or key == "Crystal" or key == "D" or key == "C":
            print("输入的是标准的VASP结构文件");
        else:
            print("输入的不是标准的VASP结构文件");
            sys.exit(0)
    except IndexError:
        print("输入的不是标准的VASP结构文件");
        sys.exit(0)
    prefix = "";
    for i in range(0, len(linecache.getline(FileName, 6).split())):
        prefix = prefix + linecache.getline(FileName, 6).split()[i] + linecache.getline(FileName, 7).split()[
            i]  # 材料化学式，元素
    constant_list = [];
    for i in [3, 4, 5]:
        constant_number = linecache.getline(FileName, i).split();
        constant = 0;
        for j in range(3):
            constant = constant + float(constant_number[j]) ** 2
        constant_list.append(round(constant ** 0.5, 5))  ##列表中分别为A、B、C晶格参数
    atoms_numbers = list(map(int, (linecache.getline(FileName, 7)).split()))  # 将原子个数所在行整理为列表,并将列表内字符串转换为数值
    element = (linecache.getline(FileName, 6)).split()  # 将元素所在行整理为列表
    cal = 0;
    atoms_place = []
    for i in range(0, len(element)):
        for j in range(0, atoms_numbers[i]):
            atoms_place.append(linecache.getline(FileName, 9 + cal).split())
            cal += 1
    File0aj.close()
    for i in range(len(atoms_place)):
        for j in range(3):
            atoms_place[i][j] = str(round(float(atoms_place[i][j]), 5))
    return constant_list[0], constant_list[1], constant_list[2], element, atoms_numbers, atoms_place


####以A轴晶格参数、B轴晶格参数、C轴晶格参数、元素名称列表、原子数量列表、原子坐标列表集的格式返回参数
##FileName = input("输入结构文件名: ")#输入结构文件名
# VASPout=VASPread(FileName)
# print(VASPout)


def QEread(FileName):
    #########以下是验证文件名是否正确，文件是否存在
    while os.path.exists(FileName) == False:
        if FileName == '0':
            sys.exit(0)
        print("QE输入文件未找到!! 若要退出请输入数字0")
        FileName = input("重新输入QE输入文件名: ")
    else:
        File0aj = open(FileName)  # 打开QE结构文件
    try:
        key = linecache.getline(FileName, 1).split()[0]
        if key == "&CONTROL" or key == '&control':
            print("输入的是标准的QE输入文件");
        else:
            print("输入的不是标准的QE输入文件");
            sys.exit(0)
    except IndexError:
        print("输入的不是标准的QE输入文件");
        sys.exit(0)
    File0aj.seek(0, 0)
    for line in File0aj:
        if line.split()[0] == 'ibrav':  ##判断ibrav的数字
            ibrav = line.split()[2][0]
            break
    File0aj.seek(0, 0)
    if ibrav == '0':
        pass;
    if ibrav == '4':  ###当ibrav=4的时候
        for line in File0aj:
            if line.split()[0] == 'A' and len(line.split()) == 3:
                A_constant = round(float(line.split()[2][0:-1]), 5)
            if line.split()[0] == 'C' and len(line.split()) == 3:
                C_constant = round(float(line.split()[2][0:-1]), 5)
                if A_constant != None:
                    break
        B_constant = A_constant
    if ibrav != '4':
        print("该结构ibrav不等于4，请手动输入晶格参数")
        A_constant = round(float(input('请输入A轴晶格参数')), 5);
        B_constant = round(float(input('请输入B轴晶格参数')), 5)
        C_constant = round(float(input('请输入C轴晶格参数')), 5)

    place_element = 1;
    File0aj.seek(0, 0)  ##文件指针回头
    for line in File0aj:  ##定位元素符号
        if 'ATOMIC_SPECIES' in line:
            break;
        else:
            place_element += 1;
    atomic_positions = 1;
    File0aj.seek(0, 0)  ##文件指针回头
    for line in File0aj:
        if 'ATOMIC_POSITIONS' in line:
            break;
        else:
            atomic_positions += 1
    ntyp = atomic_positions - place_element - 1;
    kpoint_place = 1;
    File0aj.seek(0, 0)
    element = [];
    atoms_number = [];
    atoms_place = []  ##主要输出参数初始化
    for line in File0aj:
        if 'K_POINTS' in line:
            break;
        else:
            kpoint_place += 1
    for i in range(0, ntyp):  # 元素名称列表
        element.append((linecache.getline(FileName, place_element + i + 1)).split()[0])
    for j in range(0, len(element)):
        i_element_atoms = 0
        for i in range(0, kpoint_place - atomic_positions - 1):
            if element[j] == str(linecache.getline(FileName, atomic_positions + i + 1).split()[0]):
                i_element_atoms += 1
                atoms_place.append(linecache.getline(FileName, atomic_positions + i + 1).split()[1:])
        atoms_number.append(i_element_atoms)
    return A_constant, B_constant, C_constant, element, atoms_number, atoms_place
    File0aj.close()


####以A轴晶格参数、C轴晶格参数、元素名称列表、原子数量列表、原子坐标列表集的格式返回参数
##FileName = input("输入结构文件名: ")#输入结构文件名
##QEout=QEread(FileName)
##print(QEout)

def QEwrite(data, FileName):
    #####写入QE结构文件
    ######其中输入参数data结构为A轴晶格参数、C轴晶格参数、元素名称列表、原子数量列表、原子坐标列表集
    prefix = "";
    for i in range(0, len(data[3])):
        prefix = prefix + data[3][i] + str(data[4][i])  # 元素
    with open(FileName, 'w') as File0bj:
        File0bj.write(
            "&CONTROL \n\t calculation = 'vc-relax',\n\t prefix = %s,\n\t pseudo_dir = '/home/fpzheng/software/QE/pseudo/QE_official',\n\t outdir = './outdir',\n\t tprnfor = .true.,\n\t tstress = .true.,\n\t forc_conv_thr = 4.0d-4,\n/\n" % (
                prefix))
        File0bj.write("&SYSTEM\n\t input_dft = 'vdw-df2-b86r',\n\t ");
        ibrav = float(input("请输入拟输出文件的ibrav的值"))
        if ibrav == 4:
            File0bj.write("\n\t A = %f,\n\t C = %f," % (data[0], data[2],))
        if ibrav != 4:  #########后续若要修改ibrav，在此处添加修改
            A = float(input("请输入A的值"));
            B = float(input("请输入B的值"));
            C = float(input("请输入C的值"));
            File0bj.write("\n\t A = %f,\n\t C = %f,\n\t C = %f," % (A, B, C))
        File0bj.write("\n\t nat = %d,\n\t ntyp= %d\n\t " % (sum(data[4]), (len(data[3]))))
        File0bj.write(
            "occupations = 'smearing', smearing = 'cold', degauss = 1.0d-2,\n\t ecutwfc= 50,\n\t ecutrho = 400,\n/\n&ELECTRONS\n\t electron_maxstep = 100,\n\t conv_thr = 1.0d-8,\n\t ")
        File0bj.write(
            "mixing_mode = 'plain',\n!\t mixing_beta = 0.8d0,\n\t diagonalization = 'david',\n/\n&IONS\n\t ion_dynamics='bfgs',\n/\n&CELL\n\t cell_dynamics='bfgs',\n\t cell_dofree='2Dxy',\n\t ")
        File0bj.write("press=0.0\n!\t press_conv_thr=0.1,\n/\nATOMIC_SPECIES");
        for i in range(0, len(data[3])):
            File0bj.write("\n" + data[3][i] + "\t\t\t" + data[3][i] + ".pbe-mt_fhi.UPF")
        File0bj.write("\nATOMIC_POSITIONS {crystal}");
        cal = 0
        for i in range(0, len(data[3])):
            for j in range(0, data[4][i]):
                File0bj.write("\n%s" % (data[3][i]))
                for k in range(0, 3):
                    File0bj.write("\t" + data[5][cal][k])
                cal += 1
        File0bj.write("\nK_POINTS {automatic}\n10\t10\t1\t0\t0\t0")
    File0bj.close()


def VASPwrite(data, FileName, lattice=[[1, 0, 0], [-0.5, 0.86, 0], [0, 0, 1]]):
    ########写入QE结构文件
    ######其中输入参数data结构为A轴晶格参数、C轴晶格参数、元素名称列表、原子数量列表、原子坐标列表集
    with open(FileName, 'w') as File0bj:
        File0bj.write("this file was made for VASP calculation\n1.00000\n")
        if lattice == []:
            print("目前晶体结构的a、b、c轴晶格参数为%0.8f，%0.8f，%0.8f" % (data[0], data[1], data[2]))
            print("请输入新结构在直角坐标系上的晶格矢量方向");
            number = ['x', 'y', 'z'];
            direction = ['1', '2', '3'];
            vector = [];
            lattice = []
            for i in direction:
                vector = [];
                for j in number:
                    while (True):
                        try:
                            lattice_weight = float(input('请输入第%s个晶格矢量在%s方向上的分量,分量大小需在-1到1之间\n' % (i, j)))
                        except ValueError:
                            print('请输入符合要求的数字')
                            continue
                        if -1 <= lattice_weight <= 1:
                            break;
                    vector.append(lattice_weight)
                lattice.append(vector)
            print('新结构的晶体矢量分量为');
            print(lattice)
        for i in range(3):
            for j in range(3):
                File0bj.write(str(data[i] * lattice[i][j]) + '\t')
            File0bj.write('\n')
        for i in range(0, len(data[3])):
            File0bj.write('  ' + data[3][i])
        File0bj.write('\n')
        for i in range(0, len(data[4])):
            File0bj.write('  ' + str(data[4][i]))
        File0bj.write('\nDirect\n')
        for i in range(0, len(data[5])):
            for j in range(0, 3):
                File0bj.write("\t" + data[5][i][j])
            File0bj.write('\n')


def cifread(FileName):
    #############################从cif文件里读取信息##############
    while os.path.exists(FileName) == False:
        if FileName == '0':
            sys.exit(0)
        print("cif结构文件未找到!! 若要退出请输入数字0")
        FileName = input("重新输入结构文件名: ")
    else:
        File0aj = open(FileName)  # 打开结构文件
    try:
        key = linecache.getline(FileName, 3).split()
        if key[1] == "CRYSTAL" and key[2] == "DATA":
            print("输入的是标准的cif结构文件");
        else:
            print("输入的不是标准的cif结构文件");
            sys.exit(0)
    except IndexError:
        print("输入的不是标准的cif结构文件");
        sys.exit(0)
    #######关键参数收集#####
    for line in File0aj:
        if '_cell_length_a' in line:
            A_constant = float(line.split()[1])
        if '_cell_length_c' in line:
            C_constant = float(line.split()[1])
    _line = 1;
    File0aj.seek(0, 0)
    for line in File0aj:  ##定位元素符号
        if '_atom_site_type_symbol' in line:
            atom_line = _line;
        else:
            _line += 1;
    atoms_place = [];
    element = [];
    atoms_numbers = [];
    atoms_number = 1
    for i in range(atom_line + 1, _line + 1):
        atoms_place.append(linecache.getline(FileName, i).split()[2:5])
        if linecache.getline(FileName, i).split()[-1] not in element:
            element.append(linecache.getline(FileName, i).split()[-1])
            if len(element) == 1:
                pass;
            else:
                atoms_numbers.append(atoms_number)
                atoms_number = 1
        else:
            atoms_number += 1
    atoms_numbers.append(atoms_number)
    return A_constant, C_constant, element, atoms_numbers, atoms_place
