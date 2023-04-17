#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 20:16
# @Author  : wenkaihao
# @File    : Motor.py
# @Description : Motor类
from window_ui import *
from ClassSer import *
import numpy as np


class Motor(Ui_MainWindow):

    def __init__(self):
        super(Motor, self).__init__()
        ## motor
        self.step_motor1 = 0.1
        self.step_motor2 = 0.1
        self.flag_motor1 = 0
        self.flag_motor2 = 0
        self.motor1_position = np.array([0])
        self.motor2_position = np.array([0])
        self.ser_motor1 = serial_port()
        self.ser_motor2 = serial_port()
        self.Motor_buttun()
        print("调用Motor-Thread初始化函数")

    def Motor_buttun(self):
        """
        关于电机的所有参数包括：【波特率，串口，电机使能】

        :return: None
        """
        self.Camera_Parameter = {'motor1_BandRate': self.comboBox, 'motor2_BandRate': self.comboBox_2,
                                 'motor1_COM': self.spinBox_Motor1_select, 'motor2_COM': self.spinBox_Motor2_select,
                                 'motor1_enable': self.checkBox_Motor1, 'motor2_enable': self.checkBox_Motor2}
        # 波特率
        self.Camera_Parameter['motor1_BandRate'].id = 'motor1_BandRate'
        self.Camera_Parameter['motor1_BandRate'].addItems(['115200', '57600', '38400', '19200', '9600'])
        self.Camera_Parameter['motor1_BandRate'].currentIndexChanged[str].connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_BandRate'].id = 'motor2_BandRate'
        self.Camera_Parameter['motor2_BandRate'].addItems(['115200', '57600', '38400', '19200', '9600'])
        self.Camera_Parameter['motor2_BandRate'].currentIndexChanged[str].connect(self.ChangeParameter)
        # 串口选择
        self.Camera_Parameter['motor1_COM'].id = 'motor1_COM'
        self.Camera_Parameter['motor1_COM'].valueChanged['QString'].connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_COM'].id = 'motor2_COM'
        self.Camera_Parameter['motor2_COM'].valueChanged['QString'].connect(self.ChangeParameter)

        # 电机使能
        self.Camera_Parameter['motor1_enable'].id = 'motor1_enable'
        self.Camera_Parameter['motor1_enable'].stateChanged.connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_enable'].id = 'motor2_enable'
        self.Camera_Parameter['motor2_enable'].stateChanged.connect(self.ChangeParameter)

    def ChangeParameter(self):
        chekbox = self.sender()
        if chekbox.id == 'motor1_BandRate':
            self.ser_motor1.rate = int(chekbox.currentText())
            self.label_information.setText("motor1 rate : " + chekbox.currentText())
        if chekbox.id == 'motor2_BandRate':
            self.ser_motor2.rate = int(chekbox.currentText())
            self.label_information.setText("motor2 rate : " + chekbox.currentText())
        if chekbox.id == 'motor1_COM':
            self.ser_motor1.port = "COM" + chekbox.text()
            self.label_information.setText("Motor1 COM-ID:" + self.ser_motor1.port)
        if chekbox.id == 'motor2_COM':
            self.ser_motor2.port = "COM" + chekbox.text()
            self.label_information.setText("Motor2 COM-ID:" + self.ser_motor2.port)

        if chekbox.id == 'motor1_enable':
            # print(chekbox.isChecked())
            self.EnableMotor1(chekbox.isChecked())
        if chekbox.id == 'motor2_enable':
            # print(chekbox.isChecked())
            self.EnableMotor2(chekbox.isChecked())

    def EnableMotor1(self, state):
        if not state:
            if self.flag_motor1:
                self.ser_motor1.close_port()
            self.flag_motor1=False
            self.label_information.setText("Motor1 not enable !")
        if state:
            if self.ser_motor1.enable_port():
                self.flag_motor1=True
                # 电机1初始化
                # self.ser_motor1.send = '1OR\r'
                self.ser_motor1.senddata('1OR\r')
                self.label_information.setText("Motor1 enable success !")
                # the function #
            else:

                self.label_information.setText("Motor1 enable fail !")

    def EnableMotor2(self, state):
        if not state:
            if self.flag_motor2:
                self.Serial.close_port()
            self.flag_motor1 = False
            self.label_information.setText("Motor2 not enable !")
        if state:
            if self.ser_motor2.enable_port():
                self.flag_motor2 = True
                # self.ser_motor2.enable_port()
                self.Serial.enable_port()
                # 电机2初始化
                # self.ser_motor2.send = '\0\r'
                # self.ser_motor2.senddata('\0\r')
                self.Serial.senddata('\0\r')
                self.label_information.setText("Motor2 enable success !")
            else:
                self.label_information.setText("Motor2 enable fail !")
            # the function #
