#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/28 9:34
# @Author  : wenkaihao
# @File    : SLS_Model.py
# @Description : 这个函数是用来balabalabala自己写
import numpy as np


class FiberModel:
    # 曲线拟合数据
    def __init__(self):
        self.Ap = -0.0122
        self.Bp = -90.1341
        self.Cp = 1
        self.Dp = 18116
        self.dt = 0.02

        self.A_Matrix = np.array([[0.00, self.Cp], [0.00, self.Ap]])
        self.B_Matrix = np.array([[self.Dp, -1], [self.Bp, 0]])
        self.C_Matrix = np.array([0.00, self.Cp])
        self.D_Matrix = np.array([self.Dp, 0])

        self.Ad = np.eye(2) + self.dt * self.A_Matrix
        self.Bd = self.dt * self.B_Matrix
        self.Cd = self.C_Matrix
        self.Dd = self.D_Matrix

        self.U_k = np.zeros([2, 1])
        self.X_k = np.zeros(2, 1)
        self.Y_k = np.zeros([1, 1])

    def plot_test(self, target):
        t = 400
        k = t / self.dt
        # for i in range(int(k)):


if __name__ == '__main__':
    # a = FiberModel()
    # a.plot_test()
    c = np.zeros([2, 1])
    b = np.ones([2, 1])
    c = np.append(c, b, 1)
    c = np.append(c, b, 1)
    print(c)
    d=np.array(c[:,0]).transpose()
    print(d.T)
