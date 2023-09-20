#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 19:09
# @Author  : wenkaihao
# @File    : F_control.py
# @Description : 这个函数是用来balabalabala自己写
import numpy as np

from Plot import Plot
from PyQt5 import QtCore
from sinwave import *
from ControlFunction import *
from MPC_control.MPCWithObserver import *


class F_control(Plot, MPCWithObserver):
    def __init__(self):
        super(F_control, self).__init__()

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
        self.MPC_Q = 1e-2
        self.MPC_R = 1e4

        # Strain control
        self.Strain_current = 0
        self.flagUP = True

        # enable run
        self.pushButton_F_control.clicked.connect(self.F_control_enable)
        self.pushButton_MPC_Start.clicked.connect(self.F_control_enable2)
        self.F_control_run = False

        self.timer_F_control = QtCore.QTimer()
        self.timer_F_control.timeout.connect(self.F_control_PID)

        self.timer_F_MPC_control = QtCore.QTimer()
        self.timer_F_MPC_control.timeout.connect(self.F_control_MPC)
        print("调用F_control初始化函数")

    def F_control_button(self):
        self.F_control_Parameter = {'F_target': self.lineEdit_F_target, 'F_kp': self.lineEdit_F_target_kp,
                                    'F_ki': self.lineEdit_F_target_ki, 'F_kd': self.lineEdit_F_target_kd,
                                    'F_V': self.lineEdit_F_target_v, 'threshold_input': self.lineEdit_F_target_input,
                                    'threshold_error': self.lineEdit_F_target_error,
                                    'F_target_MPC': self.lineEdit_F_target_2, 'MPC_Q': self.lineEdit_MPC_Q,
                                    'MPC_R': self.lineEdit_MPC_R, 'MPC_V': self.lineEdit_MPC_V,
                                    'MPC_Ap': self.lineEdit_MPC_Ap, 'MPC_Bp': self.lineEdit_MPC_Bp,
                                    'MPC_Cp': self.lineEdit_MPC_Cp, 'MPC_Dp': self.lineEdit_MPC_Dp
                                    }
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

        self.F_control_Parameter['F_target_MPC'].id = 'F_target_MPC'
        self.F_control_Parameter['F_target_MPC'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_Q'].id = 'MPC_Q'
        self.F_control_Parameter['MPC_Q'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_R'].id = 'MPC_R'
        self.F_control_Parameter['MPC_R'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_V'].id = 'MPC_V'
        self.F_control_Parameter['MPC_V'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_Ap'].id = 'MPC_Ap'
        self.F_control_Parameter['MPC_Ap'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_Bp'].id = 'MPC_Bp'
        self.F_control_Parameter['MPC_Bp'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_Cp'].id = 'MPC_Cp'
        self.F_control_Parameter['MPC_Cp'].editingFinished.connect(self.F_ParameterChange)
        self.F_control_Parameter['MPC_Dp'].id = 'MPC_Dp'
        self.F_control_Parameter['MPC_Dp'].editingFinished.connect(self.F_ParameterChange)

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
        if checkbox.id == 'F_target_MPC':
            self.F_target = float(checkbox.text())
            self.label_information.setText("'F_target_MPC' :" + checkbox.text())
            print(self.F_target)
        if checkbox.id == 'MPC_Q':
            self.MPC_Q = float(checkbox.text())
            self.label_information.setText("MPC_Q :" + checkbox.text())
            print(self.MPC_Q)
        if checkbox.id == 'MPC_R':
            self.MPC_R = float(checkbox.text())
            self.label_information.setText("MPC_R :" + checkbox.text())
            print(self.MPC_R)
        if checkbox.id == 'MPC_V':
            self.F_v = float(checkbox.text())
            self.label_information.setText("MPC_V :" + checkbox.text())
            print(self.F_v)
        if checkbox.id == 'MPC_Ap':
            self.Ap = float(checkbox.text())
            self.label_information.setText("MPC_Ap :" + checkbox.text())
            print(self.Ap)
        if checkbox.id == 'MPC_Bp':
            self.Bp = float(checkbox.text())
            self.label_information.setText("MPC_Bp :" + checkbox.text())
            print(self.Bp)
        if checkbox.id == 'MPC_Cp':
            self.Cp = float(checkbox.text())
            self.label_information.setText("MPC_Cp :" + checkbox.text())
            print(self.Cp)
        if checkbox.id == 'MPC_Dp':
            self.Dp = float(checkbox.text())
            self.label_information.setText("MPC_Dp :" + checkbox.text())
            print(self.Dp)

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

    def F_control_enable2(self):
        if not self.F_control_run:
            self.MPC_sum_error = 0
            self.X_k_hat = np.zeros([2, 1])
            self.timer_F_MPC_control.start(25)
            self.pushButton_MPC_Start.setText('Stop')
            self.label_information.setText("F control MPC running  !")
            self.F_control_run = True
        else:
            self.timer_F_MPC_control.stop()
            self.MPC_sum_error = 0
            self.X_k_hat = np.zeros([2, 1])
            self.pushButton_MPC_Start.setText('Run')
            self.label_information.setText("F control MPC stop !")
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
        #     print("电机2输出指令： ", ser_motor2_send)
        # print("电机2中心位置 ", self.MCenter)
        # print("F current ", self.F_current)
        # print("F error", self.F_error)
        # print("F_control_signal ", self.F_control_signal)
        # print("sum_error", self.sum_error)

    def F_control_MPC(self):
        print('------------------')
        current_time = datetime.now()
        print(current_time)
        self.F_current = self.img_F_plot[-1]
        self.F_error = (self.F_target - self.F_current)
        if abs(self.F_error) < self.F_threshold_error:
            self.F_control_signal = 0
        else:
            # 首先读取当前的输入
            u_current_1 = self.MCenter-self.Motor2Plot[-1]
            u_current_2 = self.F_target
            u_current = np.array([[u_current_1], [u_current_2]])
            print("U-current-input", u_current)
            print("Motor2 Position ",self.Motor2_position)
            y_current = np.array([[self.F_current]])

            x_next_hat = self.L_Observer(u_current, y_current, self.X_k_hat[:, -1].reshape(2, 1), self.F_target)
            self.X_k_hat = np.append(self.X_k_hat, x_next_hat, 1)
            # MPC control
            u_input = self.MPC_control(self.X_k_hat[:, -1].reshape(2, 1), self.F_target,self.MPC_Q,self.MPC_R)
            u_inputMotor = u_input[0, 0]
            print("MPC U-Input", u_inputMotor)
            temp_IX = (self.x_center - self.cx) * self.pixel_to_distance / 1000
            MotorIput = self.MCenter - (u_inputMotor + 0*temp_IX)
            if abs(u_inputMotor) > self.F_threshold_input:
                MotorIput = self.MCenter-self.F_threshold_input
            temp = "MOVEABS %.3f" % MotorIput
            temp += ' ' + str(self.F_v)
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            self.request_msg(ser_motor2_send)
            print("电机2输出指令： ", ser_motor2_send)
            print("电机2中心位置 ", self.MCenter)
            print("F current ", self.F_current)
            print("F error", self.F_error)
            print("F target",self.F_target)
            print("MotorIput ", MotorIput)

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
    print("ok")
