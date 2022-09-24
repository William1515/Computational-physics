import linecache
import numpy as np
import math
import sys

try:
    file_name_temp = sys.argv[1]
except:
    print("Failed to find file.'")
    file_name_temp = input("Please enter the file name angin:")
finally:
    file_name = file_name_temp

try:
    fp = open(file_name, 'r+')
except:
    print("Failed to open file, please check your input.")
    sys.exit(1)


# 求两向量间夹角，即晶胞轴角
def vec_angle(v1, v2):
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    cos_angle = np.dot(v1, v2) / (l1 * l2)

    angle = np.arccos(cos_angle)
    # 单位是Π
    return angle / math.pi


# 分数比较，精度为0.001，在精度内相等则返回True
def fraction_compare(a1, a2):
    if abs(a1 - a2) <= 0.001:
        return True
    else:
        return False


# 打开POSCAR文件
file = open(file_name)
# 读取POSCAR文件
# constant_list为A,B,C晶格参数
constant_list = []
# 创建3*3的二维数组用于存储基矢信息
constant_array = np.zeros([3, 3])
for i in [3, 4, 5]:
    constant_number = linecache.getline(file_name, i).split()
    constant = 0
    for j in range(3):
        constant = constant + float(constant_number[j]) ** 2
        constant_array[i - 3, j] = float(constant_number[j])
    constant_list.append(round(constant ** 0.5, 5))

# 创建1*3的数列储存轴角信息
angle_list = [round(vec_angle(constant_array[1], constant_array[2]), 5),  # alpha
              round(vec_angle(constant_array[0], constant_array[2]), 5),  # beta
              round(vec_angle(constant_array[0], constant_array[1]), 5)]  # gamma

# print(vec_angle(constant_array[0], constant_array[1]))

ibrav = 0

# ibrav = 1
if angle_list[0] == angle_list[1] == angle_list[2] == 0.5 and constant_array[0] == constant_array[1] == constant_array[2]:
    ibrav = 1


# ibrav = 4
if angle_list[0] == angle_list[1] == 0.5 and fraction_compare(angle_list[2], 2 / 3) and constant_list[0] == constant_list[1]:
    ibrav = 4

# ibrav = 6
if angle_list[0] == angle_list[1] == 0.5 and angle_list[1] != angle_list[2] and constant_list[0] == constant_list[1]== constant_list[2]:
    ibrav = 6

# ibrav = 8
if angle_list[0] == angle_list[1] == angle_list[2] and constant_list[0] != constant_list[1] and constant_list[1] != constant_list[2] and constant_list[1] != constant_list[0]:
    ibrav = 8

# ibrav = 12
if angle_list[0] == angle_list[2] == 0.5 and fraction_compare(angle_list[2], 2 / 3) == 0 and constant_list[0] != constant_list[1] and constant_list[1] != constant_list[2] and constant_list[1] != constant_list[0]:
    ibrav = 12

# ibrav = 14
if constant_list[0] != constant_list[1] and constant_list[1] != constant_list[2] and constant_list[1] != constant_list[0] and angle_list[0] != angle_list[1] and angle_list[1] != angle_list[2] and angle_list[0] != angle_list[2]:
    ibrav = 14

print("ibrav = %d" % ibrav)



# 获取晶胞中的原子信息
atom_total = 0
atom_name   = linecache.getline(file_name, 6).split()
atom_specie = linecache.getline(file_name, 7).split()  # 各类原子的数量的列表
for i in range(len(atom_specie)):
    atom_total = atom_total + int(atom_specie[i])
nat = atom_total                               # 原子总数
ntyp = len(atom_specie)                        # 原子种类数

# 输出QE文件
fp = open("./POSCAR_to_QE.scf", "w")
print(
    """&CONTROL
...
/ 
&system
    ibrav = %d""" % ibrav, file=fp
)

# 输出system中的celldm参数
if ibrav == 4:
    print(
        """\tA = %f
    C = %f
    nat = %d
    ntyp = %d
        """ % (constant_list[0], constant_list[2], nat, ntyp), file = fp
    )

print(
    """&electrons
...
/ 
&IONS
...
/
&CELL
...   
/
""", file=fp
)

# 将晶胞矢量输出到文件中
# np.savetxt(fp, constant_array, fmt='%f', delimiter=' ')

print(
    """ATOMIC_POSITIONS crystal""", file=fp
)

k = 0
# 将晶胞中的原子信息输出到文件中
for i in range(ntyp):                                               # 每一类原子
    for j in range(int(atom_specie[i])):                            # 一类原子中的每一个原子
        print("""%s """ % atom_name[i], file=fp, end=' ')
        vector_temp = linecache.getline(file_name, 9 + k).split()
        for t in range(3):                                          # 一个原子的三个坐标
            print("%f " % float(vector_temp[0]), file = fp, end=' ')
        print('', file = fp)
        k = k + 1

print("Convertion done.")