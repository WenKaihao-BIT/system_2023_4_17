#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/28 9:34
# @Author  : wenkaihao
# @File    : SLS_Model.py
# @Description : 这个函数是用来balabalabala自己写
import numpy as np
import matplotlib.pyplot as plt


class FiberModel:
    # 曲线拟合数据
    def __init__(self):
        self.Ap = -0.0122
        self.Bp = -90.1341
        self.Cp = 1
        self.Dp = 18116
        self.dt = 0.025

        self.A_Matrix = np.array([[0.00, self.Cp], [0.00, self.Ap]])
        self.B_Matrix = np.array([[self.Dp, -1], [self.Bp, 0]])
        self.C_Matrix = np.array([[0.00, self.Cp]])
        self.D_Matrix = np.array([[self.Dp, 0]])

        self.Ad = np.eye(2) + self.dt * self.A_Matrix
        self.Bd = self.dt * self.B_Matrix
        self.Cd = self.C_Matrix
        self.Dd = self.D_Matrix

        self.U_k = np.zeros([2, 1])
        self.X_k = np.zeros([2, 1])
        self.Y_k = np.zeros([1, 1])
        self.X_k_hat = np.zeros([2, 1])
        print("SLS初始化函数")

    def plot_test(self, target):
        t = 400
        k = t / self.dt
        time_array = np.arange(0, t + self.dt, self.dt).T
        # time_array = np.array([time_array])
        for i in range(int(k)):
            u_next = np.array([[target], [0]])
            self.U_k = np.append(self.U_k, u_next, 1)

            x_next = self.Ad @ self.X_k[:, -1:] + self.Bd @ self.U_k[:, -1:]
            self.X_k = np.append(self.X_k, x_next, 1)

            y_next = self.Cd @ x_next + self.Dd @ u_next
            self.Y_k = np.append(self.Y_k, y_next, 1)
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(time_array, np.squeeze(self.Y_k), color='blue', linewidth=1)
        axs[0, 0].set_title('Y-K')
        axs[0, 0].set_xlabel("time/s")
        axs[0, 0].set_ylabel('F/uN')
        axs[0, 0].grid(True, linewidth=0.5, alpha=0.5)
        # 输入input
        axs[0, 1].plot(time_array, self.U_k[0, :], color='red', linewidth=1)
        axs[0, 1].set_title('U-input')
        axs[0, 1].set_xlabel("time/s")
        axs[0, 1].set_ylabel('strain')
        axs[0, 1].grid(True, linewidth=0.5, alpha=0.5)

        # 在第三个子图中绘制error
        axs[1, 0].plot(time_array, self.X_k[0, :], color='black', linewidth=1)
        axs[1, 0].set_title('Error')
        axs[1, 0].set_xlabel("time/s")
        axs[1, 0].set_ylabel('Error')
        axs[1, 0].grid(True, linewidth=0.5, alpha=0.5)
        #
        # # 在第四个子图中绘制x^2函数
        # 在第三个子图中绘制error
        axs[1, 1].plot(time_array, self.X_k[1, :], color='black', linewidth=1)
        axs[1, 1].set_title('Xp')
        axs[1, 1].set_xlabel("time/s")
        axs[1, 1].set_ylabel('Xp')
        axs[1, 1].grid(True, linewidth=0.5, alpha=0.5)
        # 调整子图之间的间距
        plt.tight_layout()
        #
        # 显示图像
        plt.show()


if __name__ == '__main__':
    a = FiberModel()
    a.plot_test(0.16)
