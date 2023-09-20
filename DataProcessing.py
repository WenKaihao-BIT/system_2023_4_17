#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 11:25
# @Author  : wenkaihao
# @File    : DataProcessing.py
# @Description : 这个函数是用来balabalabala自己写
import matplotlib.pyplot as plt

path = 'Data/09_18_21_35_01.txt'
delimiter = '@'
dt = 0.06
time = [0]
Time = []
pixel_to_distance = 5
L0 = 2
Motor1 = []
Motor2 = []
ImgX = []
ImgY = []
F = []
Strain = [0]
strain = []
Dd = [0]
Move_Motor2 = [0]
Move_ImgX = [0]
E = [0]
D = 200 / 1000000  # 米
S = 3.14 * D * D / 4
with open(path, encoding='utf-8') as file:
    content = file.readlines()

###逐行读取数据
# print(content)

for line in content:
    data = line.split('\n')[0]
    data = data.split(' ')
    if len(data) != 7:
        continue
    # time.append(round(time[-1]+dt,2))
    # print(data[5])
    Time.append(float(data[0]))
    Motor1.append(float(data[1].split(delimiter)[1]))
    Motor2.append(float(data[2].split(delimiter)[1]))
    ImgX.append(float(data[3].split(delimiter)[1]))
    ImgY.append(float(data[4].split(delimiter)[1]))
    F.append(float(data[5].split(delimiter)[1])+5)
    # F.append((float(data[5].split(delimiter)[1]))/0.6*13)
    strain.append(float(data[6].split(delimiter)[1]))
    # print(data)
    # print(line)

length = len(Motor1)
# print(length)
for i in range(0, length - 1):
    time.append(round(i * dt, 2))

# print(time)
# print(Motor1)
# print(Motor2)
# print(ImgX)
# print(ImgY)
# print(F)
# print(Strain)

# 绘制移动探针位移图
# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, Motor2)
ax.set(title='Pic-1:Motor2-Position',
       ylabel='x / mm', xlabel='time / s')

# 绘制测量拉力移图
# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, F, color='black', linewidth=1)
ax.set(title='Pic-2:F', ylabel='F / uN', xlabel='time/s')

# 绘制测量探针移动图
# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, ImgX, color='black', linewidth=1)
ax.set(title='Pic-3:ImgX', ylabel='pixel', xlabel='time / s')

for i in range(1, length):
    Move_Motor2.append(Move_Motor2[-1] + Motor2[i] - Motor2[i - 1])
    Move_ImgX.append((ImgX[i] - ImgX[i - 1]) * pixel_to_distance / 1000 + Move_ImgX[-1])  # 转换为mm的单位
    Dd.append((abs(Move_Motor2[-1]) - abs(Move_ImgX[-1])))
    Strain.append((abs(Move_Motor2[-1]) - abs(Move_ImgX[-1])) / L0)

# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, Move_Motor2, color='blue', linewidth=1)
ax.plot(Time, Move_ImgX, color='red', linewidth=1)
ax.set(title='Pic-4:Move-ImgX', ylabel='x / mm', xlabel='time / s')

# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, strain, color='black', linewidth=1)
ax.set(title='Pic-5:Strain', ylabel='strain ', xlabel='time / s')
plt.show()

# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(strain, F, color='black', linewidth=1)
ax.set(title='Pic-6:F-Strain', ylabel='F ', xlabel='strain')
plt.show()

# print(Strain)
for i in range(1, length):
    dF = F[i] - F[i - 1]
    ds = strain[i] - strain[i - 1]
    # print(ds)
    if ds == 0:
        E.append(0)
    else:
        E_now = (dF / 1000000 / S) / ds / 1000
        E.append(E_now)

# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, E, color='black', linewidth=1)
ax.set(title='Pic-7:E', ylabel='E / kPa', xlabel='time / s')
# 产生一张画布
fig = plt.figure()
# 设置图的位置 111表示 1x1的第一个
ax = fig.add_subplot(111)
ax.plot(Time, Dd, color='black', linewidth=1)
ax.set(title='Pic-8:Displacement difference', ylabel='x / mm', xlabel='time / s')

plt.show()
