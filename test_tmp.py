from abc import ABC, abstractmethod


class ui:
    def __init__(self):
        super().__init__()
        print("ui")


class camera(ui):
    def __init__(self):
        super().__init__()
        print("camera")


class ser_thread:
    def __init__(self):
        print("ser_thread")


class send(ser_thread):
    def __init__(self):
        super().__init__()
        print("send")


class receive(ser_thread):
    def __init__(self):
        super().__init__()
        print("receive")


class motor(ui,receive,send):
    def __init__(self):
        super().__init__()
        print("motor")
class A:
    def __init__(self):
        print("A's init")

class B(A):
    def __init__(self):
        super().__init__()
        print("B's init")

class C(A):
    def __init__(self):
        super().__init__()
        print("C's init")

class E:
    def __init__(self):
        super().__init__()
        print("E's init")

class D(E, B, C):
    def __init__(self):
        super().__init__()
        print("D's init")

if __name__ == '__main__':
    a = motor()
    print(motor.mro())
    d=D()
    print(D.mro())
