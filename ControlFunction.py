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


class ControlFunction(Motor):
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
        self.wave = []

        self.F_sin_A = 3000
        self.F_sin_F = 0.1
        self.F_sin_D = 0
        self.F_sin_B = 0
        self.F_wave = []
        self.F_wave_len = 0
        self.F_count = 0
        self.F_target = 0
        self.F_sin_flag = False

        self.lineEdit_sin = {'A': self.lineEdit_A, 'F': self.lineEdit_F, 'D': self.lineEdit_D, 'B': self.lineEdit_B,
                             'AF': self.lineEdit_AF, 'FF': self.lineEdit_FF, 'DF': self.lineEdit_DF,
                             'BF': self.lineEdit_BF}
        for key, item in self.lineEdit_sin.items():
            item.id = key
            item.editingFinished.connect(self.sin_get)
        self.checkBox_sin.stateChanged.connect(self.SinDataSend)
        self.checkBox_Adaptive.stateChanged.connect(self.SinRun)
        self.checkBox_Sine_F.stateChanged.connect(self.sin_F_swap)
        self.checkBox_F_sin.stateChanged.connect(self.F_sinwave)
        self.checkBox_Random.stateChanged.connect(self.M_randam)
        print("调用ControlFunction初始化函数")

    def SendData(self):
        if self.count < self.wave_len:
            temp = self.wave[self.count].split('\n')[0]
            data = temp + '<' + self.checksum(temp) + '>\r\n'
            # print(data)
            # self.ser_motor2.senddata(data)
            self.request_msg(data)
            self.count = self.count + 1
        else:
            self.count = 0
        if self.F_sin_flag:
            if self.F_count < self.F_wave_len:
                self.F_target = float(self.F_wave[self.F_count])
                print(type(self.F_target))
                self.F_count = self.F_count + 1
            else:
                self.F_count = 0
            print(self.F_target, end='')

    def SinRun(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            self.timer_send.start(10)
            self.label_information.setText("sin is running---")
            # 保存

        elif state == QtCore.Qt.Unchecked:
            self.timer_send.stop()
            self.count = 0
            self.request_clean()
            # 数据保存
            # self.save_data.close()
            self.label_information.setText("sin is stop---")

    def SinDataSend(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "sin_cmd\sin_wave_cmd.txt"
            self.wave = sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B, 100)
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
        if chekbox.id == 'AF':
            self.F_sin_A = float(self.lineEdit_AF.text())
            self.label_information.setText("sin-->AF : " + self.lineEdit_AF.text())
            # print(self.F_sin_A)
        if chekbox.id == 'FF':
            self.F_sin_F = float(self.lineEdit_FF.text())
            self.label_information.setText("sin-->FF : " + self.lineEdit_FF.text())
            # print(self.F_sin_F)
        if chekbox.id == 'DF':
            self.F_sin_D = float(self.lineEdit_DF.text())
            self.label_information.setText("sin-->DF : " + self.lineEdit_DF.text())
            # print(self.F_sin_D)
        if chekbox.id == 'BF':
            self.F_sin_B = float(self.lineEdit_BF.text())
            self.label_information.setText("sin-->BF : " + self.lineEdit_BF.text())
            # print(self.F_sin_B)

    def UserDefine(self, state):
        if state == QtCore.Qt.Checked:
            # 发送指令
            file_add = "sin_cmd\sin_wave_user_cmd.txt"
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
            file_add = "sin_cmd\sin_wave_F_swap_cmd.txt"
            # self.wave=sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B,1)
            self.wave = sin_wave_sin_F_swap(file_add, self.sin_A, self.sin_D, self.sin_B)
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
            file_add = "sin_cmd\M_randam.txt"
            # self.wave=sin_wave_cmd(file_add, self.sin_A, self.sin_F, 50, self.sin_D, self.sin_B,1)
            self.wave = mseq([1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1], file_add, L=100, dt=1 / 50)
            self.wave_len = len(self.wave)
            self.label_information.setText("M_random is running")
        elif state == QtCore.Qt.Unchecked:
            self.wave = []
            self.wave_len = 0
            self.count = 0
            self.label_information.setText("M_random is stop")

    def F_sinwave(self, state):
        if state == QtCore.Qt.Checked:
            self.F_sin_flag = True
            # 发送指令
            f_file_add = "sin_cmd\F_sin_wave_cmd.txt"
            self.F_wave = sin_wave_cmd_F(f_file_add, self.F_sin_A, self.F_sin_F, 50, self.F_sin_D, self.F_sin_B, 100)
            self.F_wave_len = len(self.F_wave)
            self.label_information.setText("sin F is running")
        elif state == QtCore.Qt.Unchecked:
            self.F_sin_flag = False
            self.F_wave = []
            self.F_wave_len = 0
            self.F_count = 0
            self.label_information.setText("sin F is stop")
