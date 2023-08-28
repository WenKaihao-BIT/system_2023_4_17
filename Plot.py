#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 10:01
# @Author  : wenkaihao
# @File    : Plot.py
# @Description : 用于创建曲线绘制类
import threading

from PyQt5 import QtCore
from Motor import Motor
import numpy as np
import datetime
from Camera_Thread import Camera_Thread
import time


class Plot(Camera_Thread, Motor):
    def __init__(self):
        super(Plot, self).__init__()
        self.curve_F = None
        self.curve_y = None
        self.curve_x = None
        self.curve_motor2 = None
        self.curve_motor1 = None
        self.curve_strain = None
        self.flag_plot = False
        self.flag_save = False
        self.file = None

        self.data_motor2 = 0
        self.motor1_plot = np.array([0])
        self.motor1_position = np.array([0])
        self.Motor2Plot = np.array([0])
        self.motor2_position = np.array([0])
        self.img_x_plot = np.array([0])
        self.img_y_plot = np.array([0])
        self.img_F_plot = np.array([0])
        self.img_strain_plot = np.array([0])

        self.DataSave = ""

        self.background_init()
        # 绘制图像时钟
        self.timer_plot = QtCore.QTimer()
        self.timer_plot.timeout.connect(self.update_data)

        # enable button
        self.pushButton_Enable.clicked.connect(self.plot_enable)
        self.pushButton_saveData.clicked.connect(self.save_data)
        self.start_flag = False
        print("调用Plot初始化函数")

    def background_init(self):
        """
        设置绘制图形的背景

        :return: None
        """
        self.graphicsView_motor1.setBackground('w')
        self.graphicsView_motor2.setBackground('w')
        self.graphicsView_F.setBackground('w')
        self.graphicsView_x.setBackground('w')
        self.graphicsView_y.setBackground('w')
        self.graphicsView_F_2.setBackground('w')

    def clear_curve(self):
        """
        清除曲线内容

        :return: None
        """
        self.graphicsView_motor1.plot(clear='clear')
        self.graphicsView_motor2.plot(clear='clear')
        self.graphicsView_x.plot(clear='clear')
        self.graphicsView_y.plot(clear='clear')
        self.graphicsView_F.plot(clear='clear')
        self.graphicsView_F_2.plot(clear='clear')

    def plot_enable(self):
        if self.flag_motor1 and self.flag_motor2:
            if not self.flag_plot:
                self.flag_plot = True
                self.pushButton_Enable.setText("Close")
                self.label_information.setText("plot enable!")
                # motor2 启动
                self.request_msg('ACTIVE<BC>\r')
                self.request_msg('en<D3>\r')
                # self.ser_motor2.senddata('ACTIVE<BC>\r')
                # self.ser_motor2.senddata('en<D3>\r')
                # 数据清除
                self.clear_curve()
                # 曲线数据
                self.curve_motor1 = self.graphicsView_motor1.plot(self.motor1_plot)
                self.curve_motor2 = self.graphicsView_motor2.plot(self.Motor2Plot)

                self.curve_x = self.graphicsView_x.plot(self.img_x_plot)
                self.curve_y = self.graphicsView_y.plot(self.img_y_plot)

                self.curve_F = self.graphicsView_F.plot(self.img_F_plot)
                self.curve_strain = self.graphicsView_F_2.plot(self.img_strain_plot)

                ## 打开时钟信号
                self.timer_plot.start(20)
                # self.timer_ReadPosition.start(50)

                # self.SendStart_flag = True
                # self.send_thread.start()
                self.Send_Receive_start(True)
            else:
                # self.SendStart_flag = False
                self.Send_Receive_start(False)
                self.pushButton_Enable.setText("Enable")
                self.clear_curve()
                self.flag_plot = 0
                self.label_information.setText("close success!")
                # motor2 关闭
                self.request_msg('ACTIVE<BC>\r')
                self.request_msg('k<6B>\r')
                # self.ser_motor2.senddata('ACTIVE<BC>\r')
                # self.ser_motor2.senddata('k<6B>\r')
                # 关闭定时器
                self.timer_plot.stop()
                # self.timer_ReadPosition.stop()
        else:
            self.label_information.setText("check!")
        pass

    def update_data(self):
        self.position_request()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f ')
        self.DataSave = dt_ms
        if self.data_motor1:
            ## 串口格式转换
            self.data_motor1 = self.data_motor1.replace('\r', '')
            self.data_motor1 = self.data_motor1.replace('1TP', '')

            # 位置显示
            self.label_distance_Motor1.setText(self.data_motor1)
            self.data_motor1 = float(self.data_motor1)
            # 添加保存
            self.DataSave += 'Motor1@' + str(self.data_motor1) + ' '

            if len(self.motor1_plot) < 150:
                self.curve_motor1.setData(self.motor1_plot)
                self.motor1_plot = np.append(self.motor1_plot, self.data_motor1)
                self.motor1_position = np.append(self.motor1_position, self.data_motor1)


            else:
                self.motor1_plot[:-1] = self.motor1_plot[1:]
                self.motor1_plot[-1] = self.data_motor1
                # 数据填充到绘制曲线中
                self.curve_motor1.setData(self.motor1_plot)
        # motor2
        self.PlotMotor2()
        # 图形 x轴坐标
        # 添加保存
        self.DataSave += 'ImgX@' + str(self.cx) + ' '
        if len(self.img_x_plot) < 150:
            self.curve_x.setData(self.img_x_plot)
            # 加入滤波器：根据经验，目标在静态会有一个像素的抖动，据此把低于一个像素视为干扰
            if abs(self.cx - self.img_x_plot[-1]) < 2:
                self.img_x_plot = np.append(self.img_x_plot, self.img_x_plot[-1])
            else:
                self.img_x_plot = np.append(self.img_x_plot, self.cx)

        else:
            self.img_x_plot[:-1] = self.img_x_plot[1:]
            if abs(self.cx - self.img_x_plot[-1]) > 2:
                self.img_x_plot[-1] = self.cx
            # 数据填充到绘制曲线中
            self.curve_x.setData(self.img_x_plot)
        # 图形 y轴坐标
        # 添加保存
        self.DataSave += 'ImgY@' + str(self.cy) + ' '
        if len(self.img_y_plot) < 150:
            self.curve_y.setData(self.img_y_plot)
            # 加入滤波器：根据经验，目标在静态会有一个像素的抖动，据此把低于一个像素视为干扰
            if abs(self.cy - self.img_y_plot[-1]) < 2:
                self.img_y_plot = np.append(self.img_y_plot, self.img_y_plot[-1])
            else:
                self.img_y_plot = np.append(self.img_y_plot, self.cy)

        else:
            self.img_y_plot[:-1] = self.img_y_plot[1:]
            if abs(self.cy - self.img_y_plot[-1]) > 2:
                self.img_y_plot[-1] = self.cy
            # 数据填充到绘制曲线中
            self.curve_y.setData(self.img_y_plot)

        # 力图像
        # 添加保存
        temp_F = -(self.cx - self.x_center) * self.k_F
        temp_IX = (self.x_center - self.cx) * self.pixel_to_distance / 1000
        temp_X = (self.MCenter - self.Motor2Plot[-1])
        temp_strain = (temp_X - temp_IX) / 5
        # print(str(temp_IX)+'---'+str(temp_X))
        # temp_strain = (self.motor2_plot[:-1]*1000-(-(self.cx - self.x_center) * self.pixel_to_distance))/10000
        self.DataSave += 'F@' + str(temp_F) + ' '
        self.DataSave += 'Strain@' + str(temp_strain) + '\n'
        if len(self.img_F_plot) < 150:
            self.curve_F.setData(self.img_F_plot)
            self.curve_strain.setData(self.img_strain_plot)
            # temp_F = -(self.cx - self.x_center) * self.k_F
            # temp_strain = (self.motor2_plot[:-1]*1000-(-(self.cx - self.x_center) * self.pixel_to_distance))/10000
            # temp_strain = (temp_X - temp_IX) / 10
            # 加入滤波器：根据经验，目标在静态会有一个像素的抖动，据此把低于一个像素视为干扰
            if abs(temp_F - self.img_F_plot[-1]) < 1 * self.k_F:
                self.img_F_plot = np.append(self.img_F_plot, self.img_F_plot[-1])
                self.img_strain_plot = np.append(self.img_strain_plot, self.img_strain_plot[-1])
            else:
                self.img_F_plot = np.append(self.img_F_plot, temp_F)
                self.img_strain_plot = np.append(self.img_strain_plot, temp_strain)

        else:
            # temp_F = -(self.cx - self.x_center) * self.k_F
            # temp_strain = -(self.cx - self.x_center) * self.pixel_to_distance
            self.img_F_plot[:-1] = self.img_F_plot[1:]
            self.img_strain_plot[:-1] = self.img_strain_plot[1:]
            if abs(temp_F - self.img_F_plot[-1]) > 1 * self.k_F:
                self.img_F_plot[-1] = temp_F
                self.img_strain_plot[-1] = temp_strain
            # 数据填充到绘制曲线中
            self.curve_F.setData(self.img_F_plot)
            self.curve_strain.setData(self.img_strain_plot)
        # 保存数据
        if self.flag_save:
            self.file.write(self.DataSave)

    def save_data(self):
        if not self.flag_save:
            self.flag_save = True
            self.pushButton_saveData.setText("Recording")
            path = "Data\\"
            name = time.strftime("%m_%d_%H_%M_%S", time.localtime())
            path_name = path + name + '.txt'
            self.file = open(path_name, 'w')

            # print(path_name)

        else:
            self.flag_save = False
            self.pushButton_saveData.setText("Save File")
            self.file.close()

    def Send_Receive_start(self, start_flag):
        if start_flag:
            self.send_thread = threading.Thread(target=self.SendRequest_run)
            self.SendStart_flag = True

            self.receive_thread = threading.Thread(target=self.ReceiveData_run)
            self.DataProcess_thread = threading.Thread(target=self.DataProcess_run)
            self.receiveStart_flag = True

            self.send_thread.start()
            self.receive_thread.start()
            self.DataProcess_thread.start()
        else:
            self.SendStart_flag = False
            self.send_thread.join()

            self.receiveStart_flag = False
            self.receive_thread.join()
            self.DataProcess_thread.join()

    def PlotMotor2(self):
        self.label_distance_Motor2.setText(self.Motor2_position)
        self.DataSave += 'Motor2@' + str(self.Motor2_position) + ' '
        self.data_motor2 = float(self.Motor2_position)
        #   绘制图形
        if len(self.Motor2Plot) < 150:
            self.curve_motor2.setData(self.Motor2Plot)
            self.Motor2Plot = np.append(self.Motor2Plot, self.data_motor2)
            # self.motor2_position = np.append(self.motor2_position, self.data_motor2)
        else:
            self.Motor2Plot[:-1] = self.Motor2Plot[1:]
            self.Motor2Plot[-1] = self.data_motor2
            # 数据填充到绘制曲线中
            self.curve_motor２.setData(self.Motor2Plot)
