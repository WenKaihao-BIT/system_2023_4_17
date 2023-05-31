#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 19:09
# @Author  : wenkaihao
# @File    : F_control.py
# @Description : 这个函数是用来balabalabala自己写

from Plot import Plot


class PID_control:
    def __init__(self):
        self.Kp = 1  # 比例常数
        self.Ki = 0  # 积分常数
        self.Kd = 0  # 微分常数

        self.last_error = 0  # 上一次误差
        self.sum_error = 0  # 误差累计

    def update(self, error):
        # 计算增量PID控制器的输出
        output = self.Kp * (error - self.last_error) + self.Ki * error + self.Kd * (
                error - 2 * self.last_error + self.sum_error)

        # 更新误差累计和上一次误差
        self.sum_error += error
        self.last_error = error

        return output


class F_control(PID_control, Plot):
    def __init__(self, target):
        super(PID_control, self).__init__()
        super(PID_control, self).update()
        self.target = target
        self.current = 0
        self.error = 0
        self.control_signal = 0
        self.threshold_error = 1 * self.k_F
        self.threshold_input = 4.5
        self.F_v = '1'

    def F_control_PID(self, v):
        self.current = self.img_F_plot[-1]
        self.error = self.target - self.current
        if self.error < self.threshold_error:
            self.control_signal = 0
        else:
            self.control_signal = self.update(self.error)
            if abs(self.control_signal) > self.threshold_input:
                self.control_signal = self.threshold_input
        temp = 'MOVEINC ' + str(self.control_signal) + ' ' + v
        ser_motor2_send = temp + '<' + self.checksum(temp) + '>\r'
        # self.ser_motor2.senddata(ser_motor2_send)


if __name__ == '__main__':
    print("F_control")
