import socket
from gpiozero import LED, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

class ctrl:
    def __init__(self):

        self.f = open("config.ini", "w")
        self.f.write("0\n0\n")
        self.f.close()

        self.AI1 = LED(22)
        self.AI2 = LED(27)
        self.BI1 = LED(5)
        self.BI2 = LED(6)
        self.PWMA = LED(17)
        self.PWMA.on()
        self.PWMB = LED(26)
        self.PWMB.on()
        self.factory = PiGPIOFactory()
        self.servo = AngularServo(18, min_angle=0, max_angle=180, pin_factory=self.factory, min_pulse_width = 0.5 / 1000, max_pulse_width = 2.5 / 1000)
        self.servo.angle = 90

        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2.connect(('142.232.234.244', 5003))
        self.connection = self.sock2.makefile('wb')

    def __del__(self):
        self.sock2.close()
        
    def forward(self):
        self.AI1.on()
        self.AI2.off()
        self.BI1.on()
        self.BI2.off()

    def backward(self):
        self.AI1.off()
        self.AI2.on()
        self.BI1.off()
        self.BI2.on()

    def left(self):
        self.AI1.off()
        self.AI2.on()
        self.BI1.on()
        self.BI2.off()

    def right(self):
        self.AI1.on()
        self.AI2.off()
        self.BI1.off()
        self.BI2.on()

    def stay(self):
        self.AI1.on()
        self.AI2.on()
        self.BI1.on()
        self.BI2.on()


    def run(self):
        while True:
            self.msg = self.sock2.recv(2048)
            if self.msg is not None:
                print(self.msg.decode())
            if "g s" in self.msg.decode():
                print('s')
                self.backward()
            elif "g w" in self.msg.decode():
                print('w')
                self.forward()
            elif "g a" in self.msg.decode():
                print('a')
                self.left()
            elif "g d" in self.msg.decode():
                print('d')
                self.right()
            elif "g l" in self.msg.decode():
                print('l')
                self.servo.angle = 0
            elif "g j" in self.msg.decode():
                print('j')
                self.servo.angle = 180
            elif "g q" in self.msg.decode():
                self.f = open("config.ini", "r")
                self.lines = self.f.readlines()
                self.f.close()
                
                self.lines = [ self.lines[0], "1\n" ]
                self.f = open("config.ini", "w")
                self.f.writelines(self.lines)
                self.f.close()
                
                print('q')

                break
            else:
                self.stay()
                self.servo.angle = 90

control = ctrl()
control.run()
