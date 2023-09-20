#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/4 9:40
# @Author  : wenkaihao
# @File    : MPCWithObserver.py
# @Description : 这个函数是用来balabalabala自己写
import numpy as np
import cvxopt
from MPC_control.SLS_Model import *
from scipy.optimize import minimize

from datetime import datetime, timedelta
import time


class MPCWithObserver(FiberModel):
    def __init__(self):
        super(MPCWithObserver, self).__init__()
        self.L = 1.1
        self.prediction_N = 5
        self.Qarray = 1 * np.array([[1, 0], [0, 1]])
        self.Rarray = 1 * np.array([[1, 0], [0, 1]])
        self.MPC_sum_error = 0
        self.error = np.array([0])
        self.A_lref = self.Ap*self.dt+1
        self.B_lref = self.Bp*self.dt
        self.C_lref = self.Cp
        self.D_lref = self.Dp
        print("MPCWithObserver 初始化函数")

    def L_Observer(self, u_current, y_current, x_current, target_current):
        A_O = self.A_lref - self.L * self.C_lref
        B_O = self.B_lref - self.L * self.D_lref
        x_next_2 = A_O * x_current[1, 0] + B_O * u_current[0, 0] + self.L * y_current[0, 0]
        # 状态变量 x
        self.MPC_sum_error = self.MPC_sum_error + self.dt * (y_current[0, 0] - target_current)
        x_next_1 = self.MPC_sum_error
        x_next_hat = np.array([[x_next_1], [x_next_2]])
        return x_next_hat

    def MPC_control(self, x_current_hat, target_current, Q, R):
        H, E = self.MPC_compute(x_current_hat, self.prediction_N, Q * self.Qarray, R * self.Rarray)
        u_next_1 = self.prediction(E, 0.5 * (H + H.T), self.prediction_N, 2)
        u_next_2 = target_current
        u_next = np.array([[u_next_1[0, 0]], [u_next_2]])

        return u_next

    def prediction(self, E, H, N, p):
        N = N - 1
        k = H.size[1] // 2
        A, b = self.create_constraint(k, 7)
        G = cvxopt.matrix(A)
        h = cvxopt.matrix(b)

        # 求解二次规划问题
        solution = cvxopt.solvers.qp(H, E, G, h)
        U_N = solution['x']
        U_N = np.array(U_N[0:p, :])
        u_next = U_N[0:p, :]
        # print(solution['primal objective'])
        return u_next

    def MPC_compute(self, x_current, N, Q, R):
        n = self.Ad.shape[0]
        p = self.Bd.shape[1]
        QX = self.createDiagonalMatrix(Q, N)
        RU = self.createDiagonalMatrix(R, N - 1)
        M_N, C_N = self.createCombinedMatrix(self.Ad, self.Bd, N - 1)
        QP_1 = C_N.T @ QX @ C_N + RU
        QP_2 = 2 * x_current.T @ M_N.T @ QX @ C_N
        QP_2 = QP_2.T
        QP_1 = cvxopt.matrix(QP_1)
        QP_2 = cvxopt.matrix(QP_2)
        return QP_1, QP_2

    def createDiagonalMatrix(self, D, N):
        # 计算新矩阵的大小
        new_shape = (D.shape[0] * N, D.shape[1] * N)

        # 创建新矩阵
        result = np.zeros(new_shape)

        # 填充新矩阵
        for i in range(N):
            row_start = i * D.shape[0]
            row_end = (i + 1) * D.shape[0]
            col_start = i * D.shape[1]
            col_end = (i + 1) * D.shape[1]
            result[row_start:row_end, col_start:col_end] = D

        return result

    def createCombinedMatrix(self, A, B, N):
        n = A.shape[0]  # A 是 n x n 矩阵，得到 n
        p = B.shape[1]  # B 是 n x p 矩阵，得到 p

        # 初始化 M 矩阵
        M = np.vstack((np.eye(n), np.zeros((N * n, n))))  # M 矩阵是 (N+1)n x n的，上面是 n x n 个 "I"

        # 初始化 C 矩阵
        C = np.zeros(((N + 1) * n, N * p))

        tmp = np.eye(n)  # 定义一个 n x n 的单位矩阵

        # 更新 M 和 C
        for i in range(1, N + 1):
            rows = slice(i * n, (i + 1) * n)  # 定义当前行数，从 i * n 开始，共 n 行

            C[rows, :] = np.hstack((tmp @ B, C[rows.start - n:rows.stop - n, :-p]))  # 将 C 矩阵填满

            tmp = A @ tmp  # 每一次将 tmp 左乘一次 A

            M[rows, :] = tmp  # 将 M 矩阵写满

        return M, C

    def create_constraint(self, N, C):
        A = np.zeros((N, 2 * N))

        # 设置对角线上的元素为 1
        for i in range(N):
            A[i, 2 * i] = 1

        b1 = C * np.ones((N, 1))
        b2 = np.zeros((N, 1))

        A = np.vstack((A, -A))
        b = np.vstack((b1, b2))

        return A, b

    def simulation_test(self, target, Q, R):
        t = 5
        k = t / self.dt
        time_array = np.arange(0, t + self.dt, self.dt).T
        # time_array = np.array([time_array])
        for i in range(int(k)):
            u_current = self.U_k[:, -1].reshape(2, 1)
            x_current = self.X_k[:, -1].reshape(2, 1)

            y_current = self.Cd @ x_current + self.Dd @ u_current
            # print(y_current)
            self.Y_k[0, -1] = y_current
            self.Y_k = np.append(self.Y_k, np.array([[0]]), 1)
            error = target - y_current
            self.error = np.append(self.error, error)

            x_next = self.Ad @ x_current + self.Bd @ u_current
            self.X_k = np.append(self.X_k, x_next, 1)

            # MPC control
            x_next_hat = self.L_Observer(u_current, y_current, self.X_k_hat[:, -1].reshape(2, 1), target)
            self.X_k_hat = np.append(self.X_k_hat, x_next_hat, 1)
            u_next = self.MPC_control(self.X_k_hat[:, -1].reshape(2, 1), target, Q, R)
            self.U_k = np.append(self.U_k, u_next, 1)
            print(datetime.now())

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
        axs[1, 0].plot(time_array, self.error, color='black', linewidth=1)
        axs[1, 0].set_title('Error')
        axs[1, 0].set_xlabel("time/s")
        axs[1, 0].set_ylabel('Error')
        axs[1, 0].grid(True, linewidth=0.5, alpha=0.5)
        #
        # # 在第四个子图中绘制x^2函数
        # 在第三个子图中绘制error
        axs[1, 1].plot(time_array, self.X_k[1, :], color='black', linewidth=1)
        axs[1, 1].plot(time_array, self.X_k_hat[1, :], color='red', linewidth=1)
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
    a = MPCWithObserver()
    # H, E = a.MPC_compute(np.array([[0], [0]]), 5)
    a.simulation_test(2500, 1e-2, 1e4)
    # print(a.Y_k)
    # print(a.error)
    print(a.X_k_hat)
