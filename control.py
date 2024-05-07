import socket
from gpiozero import LED, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

import time
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit
from multiprocessing.connection import Client
import re

import pickle
import struct

import math

class ctrl:
    def __init__(self):

        self.f = open("config.ini", "w")
        self.f.write("0\n0\n")
        self.f.close()

        self.kit = MotorKit()
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
        self.kit.motor3.throttle = 0

        self.skit = ServoKit(channels=16)
        self.skit.servo[0].angle = 90
        self.skit.servo[1].angle = 90

        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2.connect(('142.232.234.243', 5003))
        self.connection = self.sock2.makefile('wb')

        self.current = time.time()
        self.point = time.time()
        self.pattern = r'\bxl: (-?\d+\.\d{3}) yl: (-?\d+\.\d{3}) xr: (-?\d+\.\d{3}) yr: (-?\d+\.\d{3}) tl: (-?\d+\.\d{3}) tr: (-?\d+\.\d{3})\b'

        self.data = b""
        self.payload_size = struct.calcsize(">L")

    def __del__(self):
        self.sock2.close()
        
    def go(self, x, y):
        if (-0.3 <= x <= 0.3 and not -0.3 <= y <= 0.3):
            self.kit.motor1.throttle = -y
            self.kit.motor2.throttle = -y
        elif (-0.3 <= y <= 0.3 and not -0.3 <= x <= 0.3):
            self.kit.motor1.throttle = x
            self.kit.motor2.throttle = -x
        elif -0.3 > x:
            self.kit.motor1.throttle = x
            self.kit.motor2.throttle = -x
        elif 0.3 < x:
            self.kit.motor1.throttle = x
            self.kit.motor2.throttle = -x
        else:
            self.kit.motor1.throttle = 0
            self.kit.motor2.throttle = 0

    def stay(self):
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0

    def position(self, x, y):
        self.skit.servo[0].angle = 90 * x + 90
        self.skit.servo[1].angle = 180 - (90 * y + 90)

    def servostay(self):
        self.skit.servo[0].angle = 90
        self.skit.servo[1].angle = 90
    
    def gunstay1(self):
        self.kit.motor3.throttle = 0

    def gunstay2(self):
        self.kit.motor4.throttle = 0

    def shoot1(self, speed):
        self.kit.motor3.throttle = -speed

    def shoot2(self, speed):
        self.kit.motor4.throttle = -speed

    def run(self):
        while True:
            self.current = time.time()

            while len(self.data) < self.payload_size:
                #print("Recv: {}".format(len(data)))
                self.data += self.sock2.recv(4096)
                #print("Done Recv: {}".format(len(data)))
            self.packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack(">L", self.packed_msg_size)[0]
            #print("msg_size: {}".format(msg_size))
            while len(self.data) < self.msg_size:
                self.data += self.sock2.recv(4096)
            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]

            self.frame=pickle.loads(self.frame_data, fix_imports=True, encoding="bytes")

            #self.msg = self.sock2.recv(4096)
            print(self.frame)

            if (~(-0.3 <= self.frame[3] <= 0.3) and ~(-0.3 <= self.frame[4] <= 0.3)):
                self.position(self.frame[4], self.frame[3])
            else:
                self.servostay()
            if (self.frame[2] > 0):
                self.shoot1(self.frame[2])
            else:
                self.gunstay1()
            if (self.frame[5] > 0):
                self.shoot2(self.frame[5])
            else:
                self.gunstay2()
            self.go(self.frame[0], self.frame[1])

control = ctrl()
control.run()
