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

# 统计完毕，开始分类
# 三边相等
if len_counter == 3:
    if angle_counter == 3:
        print("立方晶系")
    else:
        print("三方晶系")
# 两边相等
elif len_counter == 2:
    if angle_counter == 3:
        print("四方晶系")
    else:
        print("六方晶系")
# 无相等边
else:
    if angle_counter == 3:
        print("斜方晶体")
    elif angle_counter == 0:
        print("三斜晶系")
    else:
        print("单斜晶系")
