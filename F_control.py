#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 19:09
# @Author  : wenkaihao
# @File    : F_control.py
# @Description : 这个函数是用来balabalabala自己写

from Plot import Plot
from PyQt5 import QtCore
from sinwave import *
from ControlFunction import *


# class PID_control:
#     def __init__(self):
#         self.F_Kp = 1  # 比例常数
#         self.F_Ki = 0  # 积分常数
#         self.F_Kd = 0  # 微分常数
#
#         self.last_error = 0  # 上一次误差
#         self.sum_error = 0  # 误差累计
#         print("调用PID control初始化函数")
#
#     def F_update(self, error):
#         # 计算增量PID控制器的输出
#         output = self.F_Kp * (error - self.last_error) + self.F_Ki * error + self.F_Kd * (
#                 error - 2 * self.last_error + self.sum_error)
#
#         # 更新误差累计和上一次误差
#         self.sum_error += error
#         self.last_error = error
#
#         return output


class F_control(Plot, ControlFunction):
    def __init__(self):
        super().__init__()
        self.F_Kp = 1  # 比例常数
        self.F_Ki = 0  # 积分常数
        self.F_Kd = 0  # 微分常数
        self.last_error = 0  # 上一次误差
        self.sum_error = 0  # 误差累计
        self.previous_error = 0  # 上上次误差
        self.F_control_Parameter = None

        self.F_current = 0
        self.F_error = 0
        self.F_control_signal = 0
        self.F_threshold_error = 1 * self.k_F
        self.F_threshold_input = 4.5
        self.F_v = 1
        self.F_control_button()

        # Strain control
        self.Strain_current = 0
        self.flagUP = True

        # enable run
        self.pushButton_F_control.clicked.connect(self.F_control_enable)
        self.F_control_run = False

        self.timer_F_control = QtCore.QTimer()
        self.timer_F_control.timeout.connect(self.F_control_PID)
        print("调用F_control初始化函数")

    def F_control_button(self):
        self.F_control_Parameter = {'F_target': self.lineEdit_F_target, 'F_kp': self.lineEdit_F_target_kp,
                                    'F_ki': self.lineEdit_F_target_ki, 'F_kd': self.lineEdit_F_target_kd,
                                    'F_V': self.lineEdit_F_target_v, 'threshold_input': self.lineEdit_F_target_input,
                                    'threshold_error': self.lineEdit_F_target_error}
        self.F_control_Parameter['F_target'].id = 'F_target'
        self.F_control_Parameter['F_target'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['F_kp'].id = 'F_kp'
        self.F_control_Parameter['F_kp'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['F_ki'].id = 'F_ki'
        self.F_control_Parameter['F_ki'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['F_kd'].id = 'F_kd'
        self.F_control_Parameter['F_kd'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['F_V'].id = 'F_V'
        self.F_control_Parameter['F_V'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['threshold_input'].id = 'threshold_input'
        self.F_control_Parameter['threshold_input'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['threshold_error'].id = 'threshold_error'
        self.F_control_Parameter['threshold_error'].editingFinished.connect(self.F_ParameterChange)

    def F_ParameterChange(self):
        checkbox = self.sender()
        if checkbox.id == 'F_target':
            self.F_target = float(checkbox.text())
            self.label_information.setText("F_target :" + checkbox.text())
        if checkbox.id == 'F_kp':
            self.F_Kp = float(checkbox.text())

            self.label_information.setText("F_kp :" + checkbox.text())
        if checkbox.id == 'F_ki':
            self.F_Ki = float(checkbox.text())
            self.label_information.setText("F_ki :" + checkbox.text())
        if checkbox.id == 'F_kd':
            self.F_Kd = float(checkbox.text())
            self.label_information.setText("F_kd :" + checkbox.text())
        if checkbox.id == 'F_V':
            self.F_v = float(checkbox.text())
            self.label_information.setText("F_V :" + checkbox.text())
        if checkbox.id == 'threshold_input':
            self.F_threshold_input = float(checkbox.text())
            self.label_information.setText("threshold_input :" + checkbox.text())
        if checkbox.id == 'threshold_error':
            self.F_threshold_error = float(checkbox.text())
            self.label_information.setText("threshold_error :" + checkbox.text())

    def F_update(self, error):
        # 计算增量PID控制器的输出
        # output = self.F_Kp * error + self.F_Ki * self.sum_error + self.F_Kd * (
        #         error - self.last_error)
        p_out = self.F_Kp * (error - self.last_error)
        i_out = self.F_Ki * error
        d_out = self.F_Kd * (error - 2 * self.last_error + self.previous_error)
        output = p_out + i_out + d_out
        output = output / 10000
        # 限幅
        # output = min(output, self.F_threshold_input)
        # 更新误差累计和上一次误差
        self.previous_error = self.last_error
        self.last_error = error

        return output

    def F_control_enable(self):
        if not self.F_control_run:
            self.last_error = 0  # 上一次误差
            self.sum_error = 0  # 误差累计
            self.timer_F_control.start(20)
            self.pushButton_F_control.setText('Stop')
            self.label_information.setText("F control running  !")
            self.F_control_run = True
        else:
            self.timer_F_control.stop()
            self.last_error = 0  # 上一次误差
            self.sum_error = 0  # 误差累计
            self.pushButton_F_control.setText('Run')
            self.label_information.setText("F control stop !")
            self.F_control_run = False

    def F_control_PID(self):
        print('------------------')
        self.F_current = self.img_F_plot[-1]
        self.F_error = (self.F_target - self.F_current)
        if abs(self.F_error) < self.F_threshold_error:
            self.F_control_signal = 0
        else:
            self.F_control_signal = self.F_update(self.F_error)
            if abs(self.F_control_signal) > self.F_threshold_input:
                self.F_control_signal = self.F_threshold_input
            temp = "MOVEABS %.3f" % (self.Motor2Plot[-1] - self.F_control_signal)
            temp += ' ' + str(self.F_v)
            # temp = 'MOVEABS ' + str(self.MCenter - self.F_control_signal) + ' ' + str(self.F_v)
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            self.request_msg(ser_motor2_send)
            # self.ser_motor2.senddata(ser_motor2_send)
            print(ser_motor2_send)
        print(self.MCenter)
        print(self.F_current)
        print(self.F_error)
        print(self.F_control_signal)
        print(self.sum_error)

    def Strain_Control_PID(self):
        self.Strain_current = self.img_strain_plot[-1]
        if self.flagUP:
            temp = 'MOVEINC ' + '-0.2 ' + str(self.F_v)
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            print(ser_motor2_send)
            self.ser_motor2.senddata(ser_motor2_send)
        if self.Strain_current > 0.12:
            self.flagUP = False
        if not self.flagUP:
            temp = 'MOVEINC ' + '0.2 ' + str(self.F_v)
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            print(ser_motor2_send)
            self.ser_motor2.senddata(ser_motor2_send)
        if self.Strain_current < 0.02:
            self.flagUP = True


if __name__ == '__main__':
    print("F_control")
