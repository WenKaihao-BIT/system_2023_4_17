#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 19:41
# @Author  : wenkaihao
# @File    : ControlFunction.py
# @Description : 这个函数是用来balabalabala自己写
from window_ui import Ui_MainWindow
from Motor import Motor
from PyQt5 import QtCore
from sinwave import *

class ControlFunction(Motor, Ui_MainWindow):
    def __init__(self):
        super(ControlFunction, self).__init__()
        self.timer_send = QtCore.QTimer()
        self.timer_send.timeout.connect(self.SendData)
        self.count = 0
        self.wave_len = 0
        self.sin_A = 0.3
        self.sin_F = 1
        self.sin_D = 0
        self.sin_B = 0
        self.lineEdit_sin = {'A': self.lineEdit_A, 'F': self.lineEdit_F, 'D': self.lineEdit_D, 'B': self.lineEdit_B}
        for key, item in self.lineEdit_sin.items():
            item.id = key
            item.editingFinished.connect(self.sin_get)
        self.checkBox_sin.stateChanged.connect(self.SinDataSend)
        self.checkBox_Adaptive.stateChanged.connect(self.SinRun)
        self.checkBox_Sine_F.stateChanged.connect(self.sin_F_swap)
        self.checkBox_user.stateChanged.connect(self.UserDefine)
        self.checkBox_Random.stateChanged.connect(self.M_randam)

    def SendData(self):
        if self.count < self.wave_len:
            temp = self.wave[self.count].split('\n')[0]
            data = temp + '<' + self.checksum(temp) + '>\r\n'
            # print(data)
            self.ser_motor2.senddata(data)
            self.count = self.count + 1
        else:
            self.count = 0

    def SinRun(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            self.timer_send.start(20)
            self.label_information.setText("sin is running---")
            # 保存

        elif state == QtCore.Qt.Unchecked:
            self.timer_send.stop()
            self.count = 0
            # 数据保存
            # self.save_data.close()
            self.label_information.setText("sin is stop---")

    def SinDataSend(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "D:\PY_Project\python_2022_8_3\sin_wave_cmd.txt"
            self.wave = sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B, 1)
            self.wave_len = len(self.wave)
            self.label_information.setText("sin is running")
        elif state == QtCore.Qt.Unchecked:
            self.wave = []
            self.wave_len = 0
            self.count = 0
            self.label_information.setText("sin is stop")

    def sin_get(self):
        chekbox = self.sender()
        # print(chekbox)
        if chekbox.id == 'A':
            self.sin_A = float(self.lineEdit_A.text())
            self.label_information.setText("sin-->A : " + self.lineEdit_A.text())
            # print(self.sin_A)
        if chekbox.id == 'F':
            self.sin_F = float(self.lineEdit_F.text())
            self.label_information.setText("sin-->F : " + self.lineEdit_F.text())
            # print(self.sin_F)
        if chekbox.id == 'D':
            self.sin_D = float(self.lineEdit_D.text())
            self.label_information.setText("sin-->D : " + self.lineEdit_D.text())
            # print(self.sin_D)
        if chekbox.id == 'B':
            self.sin_B = float(self.lineEdit_B.text())
            self.label_information.setText("sin-->B : " + self.lineEdit_B.text())
            # print(self.sin_B)

    def UserDefine(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "D:\PY_Project\python_2022_8_3\sin_wave_user_cmd.txt"
            # self.wave=sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B,1)
            self.wave = sin_wave_user_cmd(file_add, 10)
            self.wave_len = len(self.wave)
            self.label_information.setText("sin-user is running")
        elif state == QtCore.Qt.Unchecked:
            self.wave = []
            self.wave_len = 0
            self.count = 0
            self.label_information.setText("sin-user is stop")

    def sin_F_swap(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "D:\PY_Project\python_2022_8_3\sin_wave_F_swap_cmd.txt"
            # self.wave=sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B,1)
            self.wave = sin_wave_sin_F_swap(file_add)
            self.wave_len = len(self.wave)
            self.label_information.setText("sin-swap-F is running")
        elif state == QtCore.Qt.Unchecked:
            self.wave = []
            self.wave_len = 0
            self.count = 0
            self.label_information.setText("sin-swap-F is stop")

    def M_randam(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "D:\PY_Project\python_2022_8_3\M_randam.txt"
            # self.wave=sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B,1)
            self.wave = mseq([1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1], file_add, L=100, dt=1 / 50)
            self.wave_len = len(self.wave)
            self.label_information.setText("M_random is running")
        elif state == QtCore.Qt.Unchecked:
            self.wave = []
            self.wave_len = 0
            self.count = 0
            self.label_information.setText("M_random is stop")

