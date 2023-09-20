#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 16:40
# @Author  : wenkaihao
# @File    : Send_Thread.py
# @Description : 这个函数是用来balabalabala自己写
import datetime

from ClassSer import *
import threading
import time
import queue


class SerThread:
    def __init__(self):
        super(SerThread, self).__init__()
        # 利用一个队列来存储请求
        self.request_queue_lock = threading.Lock()
        self.request_queue = queue.Queue()
        # 利用字符串进行缓存
        self.ReceiveCache = ""
        self.ReceiveCacheLen = 5000
        self.receive_lock = threading.Lock()
        self.ser_motor2 = serial_port()
        print("SerThread初始化")


class SendRequest(SerThread):
    def __init__(self):
        super(SendRequest, self).__init__()
        self.send_thread = None
        self.SendStart_flag = False
        print("SendRequest初始化")

    def SendRequest_run(self):
        print("SendRequest Thread Send started.")
        while self.SendStart_flag:
            if not self.request_queue.empty():
                self.request_queue_lock.acquire()
                msg = self.request_queue.get()
                msg = msg + 'PFB<D8>\r'
                # 发送至电机
                self.ser_motor2.senddata(msg)
                # dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f ')
                # print(dt_ms)
                self.request_queue_lock.release()
                # print(msg)
            else:
                # dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f ')
                # print(dt_ms)
                self.ser_motor2.senddata('PFB<D8>\r')
                # print("位置请求")
            time.sleep(0.018)
        print("Thread Send finished.")

    def request_msg(self, request_msg):
        self.request_queue_lock.acquire()
        self.request_queue.put(request_msg)
        self.request_queue_lock.release()

    def request_clean(self):
        self.request_queue_lock.acquire()
        while not self.request_queue.empty():
            self.request_queue.get()
        self.request_queue_lock.release()


class ReceiveData(SerThread):
    def __init__(self):
        super(ReceiveData, self).__init__()
        self.receive_thread = None
        self.DataProcess_thread = None
        self.head = "PFB<D8>"
        self.end = "[mm]"
        self.Motor2_position = '0'
        self.receiveStart_flag = False
        print("ReceiveData初始化")

    def ReceiveData_run(self):
        print("ReceiveData Thread Send started")
        while self.receiveStart_flag:
            # 将数据读取到缓存区
            data_tmp = self.ser_motor2.receivedata()
            self.receive_lock.acquire()
            if len(self.ReceiveCache) < self.ReceiveCacheLen:
                self.ReceiveCache += data_tmp
            else:
                self.ReceiveCache = ""
            self.receive_lock.release()
            time.sleep(0.02)

    def data_processing(self, data_block):
        datas = data_block.split('\n')
        position_data = datas[1].split(" ")[0]
        # print(position_data)
        return position_data

    def DataProcess_run(self):
        print("DataProcess Thread Send started")
        while self.receiveStart_flag:
            self.receive_lock.acquire()
            start_index = self.ReceiveCache.find(self.head)
            end_index = self.ReceiveCache.find(self.end)
            if start_index != -1 and end_index != -1 and start_index < end_index:
                data_block = self.ReceiveCache[start_index:end_index + len(self.end)]
                self.Motor2_position = self.data_processing(data_block)
                # dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f ')
                # print(dt_ms + '   ' + str(self.Motor2_position))
                # print(self.Motor2_position)
                self.ReceiveCache = self.ReceiveCache[end_index + len(self.end):]
            self.receive_lock.release()
            time.sleep(0.01)
