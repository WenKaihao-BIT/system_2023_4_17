import serial


class serial_port(object):
    def __init__(self):
        self.port = "COM1"
        self.rate = 115200
        self.send = ''
        self.receive = ''
    def enable_port(self):
        try:
            self.ser = serial.Serial(self.port, self.rate, timeout=0.02)
            self.ser.flushInput()
        except IOError:
            print("找不到串口")
            return False
        return True


    def close_port(self):
        self.ser.close()
    def senddata(self,data):
        self.ser.write(data.encode('utf-8'))

    def receivedata(self):
        # self.receive = self.ser.readline()
        # receive = self.ser.read_all()
        # receive = str(receive, encoding='utf-8')
        # return receive
        self.receive = self.ser.read_all()
        self.receive = str(self.receive, encoding='utf-8')
        return self.receive


if __name__ == '__main__':
    # test
    num1 = serial_port()
    num1.enable_port()
    num1.send = "3VA?\r"
    num1.senddata()
    count = 0
    while  True:
        num1.receivedata()
        if num1.receive:
            print(num1.receive)




