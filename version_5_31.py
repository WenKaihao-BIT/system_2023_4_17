# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo4_17.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys, cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ClassSer import *
from sinwave import *
import time
from pyqtgraph import PlotWidget
import numpy as np
import pyqtgraph as pq
import threading
import datetime
from Camera_Thread import Camera_Thread
from Image_process import FindTarget
from window_ui import *
from Motor import *
from Plot import Plot
from ControlFunction import ControlFunction
from F_control import F_control
class MyMainWindow(F_control,Plot,ControlFunction, Camera_Thread, Motor, Ui_MainWindow):
    def __init__(self, MainWindow):
        self.timer_send = QtCore.QTimer()  # 串口位置询问定时器
        self.setupUi(MainWindow)  # 启动Ui
        super(MyMainWindow, self).__init__()
        # self.button_connect()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MyMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())