import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from ClassSer import *
import time
import datetime
from operator import xor

matplotlib.use('TkAgg')


def plot_image(title, x, y):
    plt.title(title)
    plt.plot(x, y, 'deepskyblue')
    plt.show()
    pass


def sin_wave(A, f, fs, phi, t, b):
    '''
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params phi:  相位
    :params t:    时间长度
    :param b: 偏置
    '''
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    pos = A * np.sin(2 * np.pi * f * n * Ts + phi * (np.pi / 180)) + b
    v = 2 * np.pi * f * A * np.cos(2 * np.pi * f * n * Ts + phi * (np.pi / 180))
    return pos, v


def sin_wave_cmd(file_add, A, f, fs, phi, b, t):
    file = open(file_add, 'w')
    y, v = sin_wave(A, f, fs, phi, t, b)
    x = np.arange(0, t, 1 / fs)
    wave = []
    # plot_image(" sinx ", x, y)
    for i in range(x.size):
        if (abs(v[i] - 0.0) < 0.0001):
            # msg = "MOVEABS %.3f 0.1 \n" % (y[i])
            msg = "MOVEABS %.3f 5 \n" % (y[i])
        else:
            # msg = "MOVEABS %.3f %.3f \n" % (y[i], abs(v[i]))
            msg = "MOVEABS %.3f 5 \n" % (y[i])
        file.write(msg)
        wave.append(msg)
    file.close()
    return wave


def sin_wave_cmd_F(file_add, A, f, fs, phi, b, t):
    file = open(file_add, 'w')
    y, v = sin_wave(A, f, fs, phi, t, b)
    x = np.arange(0, t, 1 / fs)
    wave = []
    for i in range(x.size):
        msg = "%.0f\n" % (y[i])
        file.write(msg)
        wave.append(msg)
    file.close()
    return wave


def sin_wave_user_cmd(file_add, t):
    file = open(file_add, 'w')
    dt = 1 / 50
    x = np.arange(0, t, dt)
    y = np.zeros(len(x))
    v = np.zeros(len(x))
    for i in range(10):
        yi, vi = sin_wave(0.1, 0.1 * (i + 1), 1 / dt, 0, t, 0)
        y = y + yi
        v = v + vi
    plot_image('sin', x, y)
    wave = []
    # plot_image(" sinx ", x, y)
    for i in range(x.size):
        if (abs(v[i] - 0.0) < 0.0001):
            msg = "MOVEABS %.3f 0.1 \n" % (y[i + 1])
        else:
            msg = "MOVEABS %.3f %.3f \n" % (y[i], abs(v[i]))
        file.write(msg)
        wave.append(msg)
    file.close()
    return wave


def sin_wave_sin_F_swap(file_add,A,D,B):
    file = open(file_add, 'w')
    dt = 1 / 20
    # x = np.arange(0, t, dt)
    # y = np.zeros(len(x))
    # v = np.zeros(len(x))
    v = np.array([0])
    y = np.array([0])
    for i in np.arange(0.1, 5, 0.1):
        yi, vi = sin_wave(A, i, 1 / dt, D, 5 / i, B)
        y = np.append(y, yi)
        v = np.append(v, vi)

    x = np.arange(0, len(y)) * dt
    plot_image("sin_F_swap", x, y)
    plot_image("sin_F_swap", x, v)
    wave = []
    for i in range(x.size):
        msg = "MOVEABS %.3f 5 \n" % (y[i])
        file.write(msg)
        wave.append(msg)
    file.close()
    return wave


def mseq(coef, file_add, L=100, dt=1 / 50):
    file = open(file_add, 'w')
    st = coef
    backQ = xor(coef[-1], coef[-2])
    result = [int(backQ)]
    temp = []
    temp.extend(st[:-1])
    temp.insert(0, int(backQ))
    for i in range(0, L):
        backQ = xor(temp[-1], temp[-2])
        result.append(int(backQ))
        temp = temp[:-1]
        temp.insert(0, int(backQ))
    x = np.arange(0, len(result)) * dt
    # print(result)
    plot_image("M", x, result)
    wave = []
    for i in range(x.size):
        if result[i]:
            msg = "MOVEABS 0.05 5.0 \n" * 50
        else:
            msg = "MOVEABS -0.05 5.0 \n" * 50
        file.write(msg)
        wave.append(msg)
    file.close()
    return wave


if __name__ == '__main__':
    # file_add="D:\PY_Project\python_2022_8_3\sin_wave_cmd.txt"
    # file_add = "D:\PY_Project\python_2022_8_3\sin_wave_user_cmd.txt"
    # wave=sin_wave_user_cmd(file_add,10)
    file_add = "D:\PY_Project\python_2022_8_3\sin_wave_F_swap_cmd.txt"
    sin_wave_sin_F_swap(file_add)
    # M_randam(100)
    # file_add="D:\PY_Project\python_2022_8_3\M_randam.txt"
    # mseq([1,0,1,0,1,1,0,0,0,0,1], file_add,L=100, dt=1/50)
    # msg="MOVEABS 0.05 5.0 \n"*10
    # print(msg)
