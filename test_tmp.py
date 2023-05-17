import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication


class MyThread(QThread):
    sig_msg = pyqtSignal(str)
    sig_finished = pyqtSignal()

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent=parent)
        self.stop_event = False

    def run(self):
        print("in run function")
        self.stop_event = False
        while not self.stop_event:
            # 执行死循环任务
            self.sig_msg.emit("Thread is running...")
            print("Thread is running...")
            time.sleep(0.1)

        self.sig_finished.emit()

    def stop(self):
        self.stop_event = True


class MainWindow(QObject):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.thread = MyThread()
        self.thread.sig_msg.connect(self.on_msg)
        self.thread.sig_finished.connect(self.on_finished)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def on_msg(self, msg):
        print(msg)
        print("running")

    def on_finished(self):
        print("Thread finished.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.start()
    # 在需要结束线程的地方，调用 stop() 方法
    # time.sleep(5)
    # window.stop()

    # 等待线程结束
    window.thread.wait()


if __name__ == '__main__':
    main()
