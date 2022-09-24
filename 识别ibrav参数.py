import linecache
import numpy as np
import math


# 求向量模长，即晶胞轴长
def vec_len(vec):
    return np.linalg.norm(vec)


# 求两向量间夹角，即晶胞轴角
def vec_angle(v1, v2):
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    cos_angle = np.dot(v1, v2) / (l1 * l2)

    angle = np.arccos(cos_angle)

    return angle / math.pi


file_name = "./POSCAR"

# 打开POSCAR文件
file = open("./POSCAR")
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

# 先判断constant_list中有几个元素相等
len_counter = 0
if round(vec_len(constant_array[0]), 5) == round(vec_len(constant_array[1]), 5):
    len_counter += 1

if round(vec_len(constant_array[1]), 5) == round(vec_len(constant_array[2]), 5):
    len_counter += 1

if round(vec_len(constant_array[0]), 5) == round(vec_len(constant_array[2]), 5):
    len_counter += 1

# 再判断三轴角中有几个等于90°
angle_counter = 0
if vec_angle(constant_array[0], constant_array[1]) == 0.5:
    angle_counter += 1

if vec_angle(constant_array[0], constant_array[2]) == 0.5:
    angle_counter += 1

if vec_angle(constant_array[1], constant_array[2]) == 0.5:
    angle_counter += 1

# 统计每行0的个数
zero_num = [0, 0, 0]
for j in [0, 1, 2]:
    for i in constant_array[j]:
        if i == 0:
            zero_num[j] = zero_num[j] + 1

# 统计每列0的个数
constant_array_T = constant_array.T
zero_num_col = [0, 0, 0]
for j in [0, 1, 2]:
    for i in constant_array_T[j]:
        if i == 0:
            zero_num_col[j] = zero_num_col[j] + 1

# 初始化ibrav
ibrav = 0

if np.linalg.matrix_rank(constant_array) == 3:
    print("矩阵行列式不为零")

# 立方晶系

# ibrav = 1
if zero_num[0] == 2:
    if np.std(constant_list) == 0 and np.linalg.matrix_rank(constant_array) == 3:
        ibrav = 1

# ibrav = 2
if zero_num[0] == 1:
    if np.std(constant_list) == 0 and np.linalg.matrix_rank(constant_array) == 3:
        ibrav = 2

# ibrav = 3
if zero_num[0] == 0:

    a_3 = np.abs(constant_array)
    a_3 = np.std(a_3)
    rank_3 = np.linalg.matrix_rank(constant_array)
    if a_3 == 0 and rank_3 == 3:
        ibrav = 3

# ibrav = 4
if zero_num[0] == 2:
    a_4 = constant_array[0][0]
    sqrt_3 = round(math.sqrt(3)/2, 5)
    # 根号3的精度取到0.001
    diff = abs(constant_array[1][1] - sqrt_3)
    if constant_array[1][0] == -0.5*a_4 and diff <= 0.001:
        ibrav = 4





# ibrav = 6
if zero_num[0] == 2 and zero_num[1] == 2 and zero_num[2] == 2:
    if constant_array[0][0] == constant_array[1][1] and constant_array[0][0] != constant_array[2][2]:
        ibrav = 6

# ibrav = 7
if np.std(constant_list) == 0:  # 每一行范数相等
    for j in [0, 1, 2]:
        if constant_array[j][0] == constant_array[j][1] and constant_array[j][0] != constant_array[j][2]:
            ibrav = 7

# ibrav = 8
if zero_num[0] == 2 and zero_num[1] == 2 and zero_num[2] == 2:
    if constant_array[0][0] != constant_array[1][1] and constant_array[0][0] != constant_array[2][2] and constant_array[1][1] != constant_array[2][2]:
        ibrav = 8

# ibrav = 9
if zero_num[0] == 1 and zero_num[1] == 1 and zero_num[2] == 0:
    if constant_array[0][0] == -constant_array[1][0] and constant_array[0][1] == constant_array[1][1]:
        ibrav = 9

# ibrav = -9
if zero_num[0] == 1 and zero_num[1] == 1 and zero_num[2] == 0:
    if constant_array[0][0] == constant_array[1][0] and constant_array[0][1] == -constant_array[1][1]:
        ibrav = 9

# ibrav = 10
if zero_num[0] == 1 and zero_num[1] == 1 and zero_num[2] == 1:
    if zero_num_col[0] == 1 and zero_num_col[1] == 1 and zero_num_col[2] == 1:
        if np.std(constant_list) != 0:    # 每行范数不相等
            ibrav = 10

# ibrav = 11
if zero_num[0] == 0 and zero_num[1] == 0 and zero_num[2] == 0:
    abs_matrix = np.abs(constant_array[0:2, 0])
    if np.std(abs_matrix) == 0 and constant_array[0][0] != constant_array[0][1] and constant_array[0][2] != constant_array[0][1] and constant_array[0][0] != constant_array[0][2]:
        ibrav = 11

# ibrav = 12
if constant_array[0][0] != 0 and constant_array[0][1] == constant_array[0][2] == 0:
    if constant_array[2][2] != 0 and constant_array[2][1] == constant_array[2][0] == 0:
        if constant_array[1][2] == 0 and constant_array[1][1] == constant_array[1][0]:
            ibrav = 12

# ibrav = -12
if constant_array[0][0] != 0 and constant_array[0][1] == constant_array[0][2] == 0:
    if constant_array[2][1] != 0 and constant_array[2][0] == constant_array[2][2] == 0:
        if constant_array[2][1] == 0 and constant_array[2][2] == constant_array[2][0]:
            ibrav = -12

# ibrav = 13
if constant_array[0][1] == constant_array[2][1] == constant_array[1][2] == 0:
    if constant_array[0][0] == constant_array[2][0] and constant_list[0] == constant_list[2]:
        ibrav = 13

# ibrav = 14
if constant_array[0][1] == constant_array[1][2] == constant_array[0][2] == 0:
    if zero_num[0] == 2 and zero_num[1] == 1:
        ibrav = 14


print("ibrav = %d " % ibrav)

print()

# print()

# 统计完毕，开始分类
# 三边相等
# if len_counter == 3:
#     if angle_counter == 3:
#         # print("立方晶系")
#         pass
#
#
#
#
#
#     else:
#         print("三方晶系")
# # 两边相等
# elif len_counter == 2:
#     if angle_counter == 3:
#         print("四方晶系")
#     else:
#         print("六方晶系")
# # 无相等边
# else:
#     if angle_counter == 3:
#         print("斜方晶体")
#     elif angle_counter == 0:
#         print("三斜晶系")
#     else:
#         print("单斜晶系")
