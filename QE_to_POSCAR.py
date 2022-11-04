import linecache
import numpy as np
import math
import os
import string
import re
import sys

try:
    file_name_temp = sys.argv[1]
except:
    print("Failed to find file.'")
    file_name_temp = input("Please enter the file name angin:")
finally:
    file_qe = file_name_temp

try:
    fp = open(file_qe, 'r+')
except:
    print("Failed to open file, please check your input.")
    sys.exit(1)

qe_in_list = fp.readlines()

nat = 0
ntyp = 0


# 利用正则表达式逐行匹配特定的参数标注并读取所需要的信息
for i in range(len(qe_in_list)):
    if qe_in_list[i].find('ibrav') != -1:  # find函数匹配到相应字符串则返回位置，否则返回-1
        ibrav_temp = re.findall(r"\d+", qe_in_list[i])
        ibrav = int(ibrav_temp[0])

    # 读出nat，即原子总个数
    if qe_in_list[i].find('nat') != -1:
        nat_temp = re.findall(r"\d+", qe_in_list[i])
        nat = int(nat_temp[nat_temp.index(max(nat_temp))])   # 为防止nat和ntyp被放在了同一行，于是就取了他的最大值作为nat，最小值作为ntyp

    # 读出ntyp，即原子种类数
    if qe_in_list[i].find('ntyp') != -1:
        ntyp_temp = re.findall(r"\d+", qe_in_list[i])
        ntyp = int(ntyp_temp[ntyp_temp.index(min(ntyp_temp))])

    # 读出原子信息
    if qe_in_list[i].find('ATOMIC_POSITIONS') != -1:  # 'ATOMIC_POSITIONS'出现在第i行
        atom_position = []  # 储存每个原子原子坐标信息
        atom_specie_list = []  # 储存每个原子的名称信息
        each_atom_num = np.ones([1, ntyp])  # 储存每一类原子的数量
        specie = 0

        for atom in range(nat):
            atom_temp = re.findall(r"\d+.?\d+", qe_in_list[i + atom + 1])
            atom_temp1 = float(atom_temp[0])
            atom_temp2 = float(atom_temp[1])
            atom_temp3 = float(atom_temp[2])
            atom_vector_temp = [atom_temp1, atom_temp2, atom_temp3]
            atom_position.append(atom_vector_temp)
            atom_specie = re.findall(r"[A-Z][a-z]*", qe_in_list[i + atom + 1])
            atom_specie_list.append(atom_specie[0])

            if atom > 0:
                if atom_specie_list[atom] == atom_specie_list[atom - 1]:
                    temp = each_atom_num[0][specie] + 1
                    each_atom_num[0][specie] = temp
                if atom_specie_list[atom] != atom_specie_list[atom - 1]:
                    specie = specie + 1

# 对原子种类信息进行处理： [a,a,a,b,b] -> [a,b]
atom_list = []
temp = 0
for i in range(ntyp):
    atom_list.append(atom_specie_list[temp])
    temp = temp + int(each_atom_num[0][i])


# 读出celldm数据并计算三个晶矢坐标
if ibrav == 1:
    # 需要的参数是A
    for i in range(len(qe_in_list)):
        if qe_in_list[i].find(r'A =') != -1:
            A_temp = re.findall(r"\d+.\d+", qe_in_list[i])
            A = float(A_temp[0])

    vector1 = [A, 0.00, 0.00]
    vector2 = [0.00, A, 0.00]
    vector3 = [0.00, 0.00, A]

elif ibrav == 2:
    for i in range(len(qe_in_list)):
        if qe_in_list[i].find(r'A =') != -1:
            A_temp = re.findall(r"\d+.\d+", qe_in_list[i])
            A = float(A_temp[0])

    vector1 = [-A/2, 0.00, A/2]
    vector2 = [0.00,  A/2, A/2]
    vector3 = [-A/2,  A/2, 0.00]

elif ibrav == 3:
    for i in range(len(qe_in_list)):
        if qe_in_list[i].find(r'A =') != -1:
            A_temp = re.findall(r"\d+.\d+", qe_in_list[i])
            A = float(A_temp[0])
    vector1 = [ A/2,  A/2, A/2]
    vector2 = [-A/2,  A/2, A/2]
    vector3 = [-A/2, -A/2, A/2]


elif ibrav == 4:
    # 需要的是A和C
    for i in range(len(qe_in_list)):
        if qe_in_list[i].find(r'A =') != -1:
            A_temp = re.findall(r"\d+.?\d*", qe_in_list[i])
            A = float(A_temp[0])
        if qe_in_list[i].find(r'C =') != -1:
            C_temp = re.findall(r"\d+[.]?\d*", qe_in_list[i])  # 需匹配的字符应该用[]括起来
            C = float(C_temp[0])

    # 输出晶格矢量
    vector1 = [A, 0.00, 0.00]
    vector2 = [-1 * A / 2, 1.73205 * A / 2, 0.00]
    vector3 = [0.00, 0.00, C]

vector = [vector1, vector2, vector3]

print("ibrav = %d" % ibrav)

# 开始写入输出文件
fp = open("./QE_to_POACAR.vasp", "w")
print(
    """CIF file
    1.00000""", file=fp
)

np.savetxt(fp, vector, fmt='%f', delimiter=' ')
for i in range(ntyp):
    if i == ntyp - 1:
        print("\t %s " % atom_list[i], file=fp)
    else:
        print("\t %s " % atom_list[i], file=fp, end=' ')
for i in range(ntyp):
    if i == ntyp - 1:
        print("\t %d " % int(each_atom_num[0][i]), file=fp)
    else:
        print("\t %d " % int(each_atom_num[0][i]), file=fp, end=' ')
print('Direct', file=fp)
np.savetxt(fp, atom_position, fmt='%f', delimiter=' ')

print("Convertion done.")
