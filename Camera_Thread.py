import threading
import cv2
import time
from Image_process2 import FindTarget
from window_ui import *


class Camera_Thread(Ui_MainWindow):
    def __init__(self):
        super(Camera_Thread, self).__init__()
        # 创建线程
        self.camera_thread = None

        # run函数的flag
        self.flag_run = False
        self.Camera_Parameter = None
        self.cap_video = None
        self.Camera_ID = '0'
        # 目标中心点 (cx,cy)
        self.cx = 0
        self.cy = 0
        self.flag_camera = False
        self.flag_CenterSet = False
        self.img = []
        self.x_center = 400
        self.y_center = 400
        # 此处K包含两部分（像素->距离，距离->力）
        self.pixel_to_distance = 5  # 单位为微米
        # 距离->力的比例系数
        self.distance_to_F = 12  # 单位为微牛/微米
        self.k_F = self.pixel_to_distance * self.distance_to_F
        # 图形处理阈值
        self.threshold_gray = 100
        self.threshold_area = 10000
        # MainWindow = QMainWindow()
        # self.setupUi(MainWindow)
        self.CameraButton()
        print("调用Camera-Thread初始化函数")

    def CameraButton(self):
        """
        相机控件连接函数

        :return: None
        """
        # self.spinBox_Camera_select.valueChanged['QString'].connect(self.ReadParameter)
        self.pushButton_camera.clicked.connect(self.OpenCamera)
        self.Camera_Parameter = {'Camera_ID': self.spinBox_Camera_select, 'Max_threshold': self.horizontalSlider_max,
                                 'Area_threshold': self.horizontalSlider_area,
                                 'Pixel Value Distance': self.lineEdit_p_to_d,
                                 'Force Coefficient': self.lineEdit_d_to_f, 'CenterSet': self.pushButton_CenterSet}
        self.Camera_Parameter["Camera_ID"].id = "Camera_ID"
        self.Camera_Parameter["Camera_ID"].valueChanged['QString'].connect(self.ReadParameter)
        self.Camera_Parameter["Max_threshold"].id = "Max_threshold"
        self.Camera_Parameter["Max_threshold"].valueChanged.connect(self.ReadParameter)
        self.Camera_Parameter["Area_threshold"].id = "Area_threshold"
        self.Camera_Parameter["Area_threshold"].valueChanged.connect(self.ReadParameter)
        self.Camera_Parameter["Pixel Value Distance"].id = "Pixel Value Distance"
        self.Camera_Parameter["Pixel Value Distance"].editingFinished.connect(self.ReadParameter)
        self.Camera_Parameter["Force Coefficient"].id = "Force Coefficient"
        self.Camera_Parameter["Force Coefficient"].editingFinished.connect(self.ReadParameter)
        self.Camera_Parameter["CenterSet"].id = "CenterSet"
        self.Camera_Parameter["CenterSet"].clicked.connect(self.CenterSet)
        pass

    def ReadParameter(self):
        """
        读取图像参数

        :return: None
        """
        chekbox = self.sender()
        if chekbox.id == "Camera_ID":
            self.Camera_ID = chekbox.text()
            # print("相机编号为"+self.Camera_ID)
            self.label_information.setText("camera ID :" + self.Camera_ID)
        if chekbox.id == "Max_threshold":
            self.threshold_gray = chekbox.value()
            self.label_information.setText("threshold_gray :" + str(self.threshold_gray))
        if chekbox.id == "Area_threshold":
            self.threshold_area = chekbox.value()
            self.label_information.setText("threshold_Area :" + str(self.threshold_area))
        if chekbox.id == "Pixel Value Distance":
            self.pixel_to_distance = float(chekbox.text())
            self.k_F = self.k_F = float(self.pixel_to_distance) * float(self.distance_to_F)
            self.label_K_value.setText(str(self.k_F))
            self.label_information.setText("Pixel Value Distance :" + str(self.pixel_to_distance))
        if chekbox.id == "Force Coefficient":
            self.distance_to_F = float(chekbox.text())
            self.k_F = float(self.pixel_to_distance) * float(self.distance_to_F)
            self.label_K_value.setText(str(self.k_F))
            self.label_information.setText("Force Coefficient :" + str(self.distance_to_F))
        pass

    def camera_run(self):

        while self.flag_run:
            self.show_video()
            time.sleep(0.05)

    def OpenCamera(self):
        """
        打开相机

        :return: None
        """
        if not self.flag_camera:
            self.flag_camera = True
            # 打开相机
            self.cap_video = cv2.VideoCapture(int(self.Camera_ID))  # 可注释cv2.CAP_DSHOW
            # 开启进程
            # 创建camera的线程
            self.camera_thread = threading.Thread(target=self.camera_run)
            self.flag_run = True
            self.camera_thread.start()

            self.pushButton_camera.setText("Close")
            self.label_information.setText("camera open success!")

        else:
            self.flag_camera = False
            # stop 进程
            self.flag_run = False
            self.camera_thread.join()
            # 关闭相机进程
            self.label_image1.clear()
            self.label_image2.clear()
            self.cap_video.release()
            self.pushButton_camera.setText("Open")
            self.label_information.setText("close success!")
        pass

    def show_video(self):
        """
        显示显微镜视野中的图形

        :param msg: 用来测试信号触发，无实际使用
        :return: None
        """
        # print(msg)
        ret, self.img = self.cap_video.read()
        if ret:
            self.show_cv_img(self.img)
            self.image_processing(self.img)
        else:
            self.label_information.setText("No Camera")
            # self.pushButton_camera.setText("Open")

    def show_cv_img(self, img):
        """
        图像格式转换及其显示

        :param img: 传入opencv读取的图片numpy，转换为QT能显示的格式QtImg
        :return: None
        """
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(QtImg).scaled(
            self.label_image1.width(), self.label_image1.height())

        self.label_image1.setPixmap(jpg_out)

    def image_processing(self, img):
        """
        目标识别算法
        :param img: 传入opencv图像numpy

        :return: None
        """
        # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_processed, self.cx, self.cy = FindTarget(img, self.threshold_gray, self.threshold_area)
        shrink = cv2.cvtColor(img_processed, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(QtImg).scaled(
            self.label_image2.width(), self.label_image2.height())

        self.label_image2.setPixmap(jpg_out)

    def CenterSet(self):
        """
        设置位移中心

        :return: None
        """
        if not self.flag_CenterSet:
            self.flag_CenterSet = True
            self.x_center = self.cx
            self.y_center = self.cy
            self.label_Center.setText('[' + str(self.x_center) + ',' + str(self.y_center) + ']')
            self.pushButton_CenterSet.setText("Setting")
            self.label_information.setText("Setting Center!")
        else:
            self.flag_CenterSet = False
            self.pushButton_CenterSet.setText("Set")
            self.label_information.setText("Unset Center!")
        pass
