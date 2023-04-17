
class Camera_funcion:
    def ReadCamera(self):
        # self.CameraNum = self.spinBox_Camera_select.text()
        self.Camera.Camera_ID = self.spinBox_Camera_select.text()
        # print("相机编号为"+self.CameraNum)
        self.label_information.setText("camera ID :" + self.Camera.Camera_ID)
        pass
    def OpenCamera(self):
        if self.flag == 0:
            # self.cap_video = cv2.VideoCapture(int(self.Camera.Camera_ID),cv2.CAP_DSHOW)  # 可注释 (# cv2.CAP_DSHOW)
            # self.timer.start(50)
            # self.timer2.start(50)
            # 打开相机
            self.Camera.Open_Camera()
            # 触发信号
            self.Camera.Signal_Camera.connect(self.show_viedo)
            # 开启进程
            self.Camera.start()
            self.flag = 1
            self.pushButton_camera.setText("Close")
            self.label_information.setText("camera open success!")
        else:
            # 关闭相机进程
            # self.cap_video.release()
            self.Camera.Close_Camera()
            self.Camera.exec()
            # self.timer.stop()
            # self.timer2.stop()

            self.label_image1.clear()
            self.label_image2.clear()
            self.pushButton_camera.setText("Open")
            self.flag = 0
            self.label_information.setText("close success!")
        pass