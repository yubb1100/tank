import socket
from gpiozero import LED, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

import time
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

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
        self.sock2.connect(('142.232.234.244', 5003))
        self.connection = self.sock2.makefile('wb')

    def __del__(self):
        self.sock2.close()
        
    def forward(self):
        self.kit.motor1.throttle = 1
        self.kit.motor2.throttle = 1

    def backward(self):
        self.kit.motor1.throttle = -1
        self.kit.motor2.throttle = -1

    def left(self):
        self.kit.motor1.throttle = -1
        self.kit.motor2.throttle = 1

    def right(self):
        self.kit.motor1.throttle = 1
        self.kit.motor2.throttle = -1

    def stay(self):
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
        self.kit.motor3.throttle = 0
        
    def shoot(self):
        self.kit.motor3.throttle = 1

    def run(self):
        while True:
            self.msg = self.sock2.recv(2048)
            if self.msg is not None:
                pass
                #print(self.msg.decode())
            if "g s" in self.msg.decode():
                self.backward()
                #print('s')
            elif "g w" in self.msg.decode():
                self.forward()
                #print('w')
            elif "g a" in self.msg.decode():
                #print('a')
                self.left()
            elif "g d" in self.msg.decode():
                #print('d')
                self.right()
            elif "g l" in self.msg.decode():
                #print('l')
                self.skit.servo[0].angle = 0
            elif "g j" in self.msg.decode():
                #print('j')
                self.skit.servo[0].angle = 180
            elif "g p" in self.msg.decode():
                self.shoot()
            elif "g q" in self.msg.decode():
                self.f = open("config.ini", "r")
                self.lines = self.f.readlines()
                self.f.close()
                
                self.lines = [ self.lines[0], "1\n" ]
                self.f = open("config.ini", "w")
                self.f.writelines(self.lines)
                self.f.close()
                
                #print('q')

                break
            else:
                self.stay()
                #self.servo.angle = 90

control = ctrl()
control.run()
