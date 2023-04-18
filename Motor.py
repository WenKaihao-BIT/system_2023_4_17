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
        self.flag_motor1 = False
        self.flag_motor2 = False
        self.motor1_position = np.array([0])
        self.motor2_position = np.array([0])
        self.ser_motor1 = serial_port()
        self.ser_motor2 = serial_port()
        self.Motor_buttun()
        # 设置位置读取时钟
        self.timer_ReadPosition = QtCore.QTimer()
        self.timer_ReadPosition.timeout.connect(self.position_request)
        print("调用Motor-Thread初始化函数")

    def Motor_buttun(self):
        """
        关于电机的所有参数包括：【波特率，串口，电机使能】

        :return: None
        """
        self.Camera_Parameter = {'motor1_BandRate': self.comboBox, 'motor2_BandRate': self.comboBox_2,
                                 'motor1_COM': self.spinBox_Motor1_select, 'motor2_COM': self.spinBox_Motor2_select,
                                 'motor1_enable': self.checkBox_Motor1, 'motor2_enable': self.checkBox_Motor2,
                                 'motor1_StepADD': self.pushButton_Motor1_Add,
                                 'motor1_StepReduce': self.pushButton_Motor1_Reduce,
                                 'motor2_StepADD': self.pushButton_Motor2_Add,
                                 'motor2_StepReduce': self.pushButton_Motor2_Reduce,
                                 'motor1_step': self.lineEdit_Motor1, 'motor2_step': self.lineEdit_Motor2}
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

        # 电机增量式位移
        self.Camera_Parameter['motor1_StepADD'].id = 'motor1_StepADD'
        self.Camera_Parameter['motor1_StepADD'].clicked.connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_StepADD'].id = 'motor2_StepADD'
        self.Camera_Parameter['motor2_StepADD'].clicked.connect(self.ChangeParameter)

        self.Camera_Parameter['motor1_StepReduce'].id = 'motor1_StepReduce'
        self.Camera_Parameter['motor1_StepReduce'].clicked.connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_StepReduce'].id = 'motor2_StepReduce'
        self.Camera_Parameter['motor2_StepReduce'].clicked.connect(self.ChangeParameter)

        # 读取电机增量
        self.Camera_Parameter['motor1_step'].id = 'motor1_step'
        self.Camera_Parameter['motor1_step'].editingFinished.connect(self.ChangeParameter)

        self.Camera_Parameter['motor2_step'].id = 'motor2_step'
        self.Camera_Parameter['motor2_step'].editingFinished.connect(self.ChangeParameter)

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
        if chekbox.id == 'motor1_step':
            self.step_motor1 = chekbox.text()
            self.label_information.setText("Motor1 step :" + self.step_motor1)
        if chekbox.id == 'motor2_step':
            self.step_motor2 = chekbox.text()
            self.label_information.setText("Motor2 step :" + self.step_motor2)
        if chekbox.id == 'motor1_StepADD':
            ser_motor1_send = '1PR' + str(self.step_motor1) + '\r'
            self.ser_motor1.senddata(ser_motor1_send)
            self.label_information.setText("Motor1 move: -" + str(self.step_motor1))
        if chekbox.id == 'motor1_StepReduce':
            ser_motor1_send = '1PR-' + str(self.step_motor1) + '\r'
            self.ser_motor1.senddata(ser_motor1_send)
            self.label_information.setText("Motor1 move: -" + str(self.step_motor1))
        if chekbox.id == 'motor2_StepADD':
            temp = 'MOVEINC ' + str(self.step_motor2) + ' 2'
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            self.ser_motor2.senddata(ser_motor2_send)
            self.label_information.setText("Motor2 move:" + str(self.step_motor2))
        if chekbox.id == 'motor2_StepReduce':
            temp = 'MOVEINC -' + str(self.step_motor2) + ' 2'
            ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
            self.ser_motor2.senddata(ser_motor2_send)
            self.label_information.setText("Motor2 move:-" + str(self.step_motor2))

    def EnableMotor1(self, state):
        if not state:
            if self.flag_motor1:
                self.ser_motor1.close_port()
            self.flag_motor1 = False
            self.label_information.setText("Motor1 not enable !")
        if state:
            if self.ser_motor1.enable_port():
                self.flag_motor1 = True
                # 电机1初始化
                # self.ser_motor1.send = '1OR\r'
                self.ser_motor1.senddata('1OR\r')
                self.label_information.setText("Motor1 enable success !")
                # the function #
            else:

                self.label_information.setText("Motor1 enable fail !")
        # print(self.flag_motor1)
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

    def checksum(self, s):
        '''
        电机2校验码获取

        :param s: 输入字符串
        :return: 校验十六进制数的字符串
        '''
        response_hex_list = []
        for i in range(len(s)):
            response_hex_list.append(hex(ord(s[i]))[2:])
        check_sum_str = hex(sum([int(i, 16) for i in response_hex_list]))[-2:].upper()
        return check_sum_str

    def position_request(self):
        """
        用于发送和接受电机的位置信息请求

        :return: None
        """
        # self.ser_motor1.send = '1TP?\r'
        self.ser_motor1.senddata('1TP?\r')
        self.data_motor1 = self.ser_motor1.receivedata()
        # print(self.data_motor1)
        # self.ser_motor2.send = 'PFB<D8>\r'
        # self.ser_motor2.senddata('PFB<D8>\r')
        self.Serial.senddata('PFB<D8>\r')
        # self.data_motor2 = self.ser_motor2.receivedata()
        # time.sleep(0.01)
        self.data_motor2 = self.Serial.receivedata()
        data_motor2_temp = self.DataAnlysis(self.data_motor2, 'PFB<D8>')
        print('\n\n' + self.data_motor2 + '\n' + self.data_motor2.encode().hex() + '\n' + data_motor2_temp + '\n\n')
        # print('\n\n'+self.data_motor2+'\n\n')
