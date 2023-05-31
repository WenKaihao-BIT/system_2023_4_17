import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.cap = None
        self.timer = None

        # 创建GUI界面
        self.setWindowTitle('USB Camera')
        self.setFixedSize(640, 480)

        # 创建标签和按钮
        self.label = QLabel(self)
        self.btn_open = QPushButton('Open', self)
        self.btn_close = QPushButton('Close', self)
        self.btn_close.setEnabled(False)

        # 将标签和按钮添加到垂直布局中
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

        # 绑定按钮点击事件
        self.btn_open.clicked.connect(self.on_open)
        self.btn_close.clicked.connect(self.on_close)

    def on_open(self):
        # 打开相机
        self.cap = cv2.VideoCapture(0)

        # 检查相机是否打开
        if not self.cap.isOpened():
            print("Could not open camera.")
            return

        # 启动定时器以循环读取帧
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # 更新界面
        self.btn_open.setEnabled(False)
        self.btn_close.setEnabled(True)

    def on_close(self):
        # 停止定时器
        self.timer.stop()

        # 释放相机
        self.cap.release()
        self.cap = None

        # 更新界面
        self.btn_open.setEnabled(True)
        self.btn_close.setEnabled(False)
        self.label.setPixmap(QPixmap())

    def update_frame(self):
        # 读取一帧
        ret, frame = self.cap.read()

        # 检查帧是否读取成功
        if not ret:
            print("Error reading frame.")
            return

        # 将帧转换为QImage
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        img = img.rgbSwapped()

        # 在标签中显示QImage
        self.label.setPixmap(QPixmap.fromImage(img))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()