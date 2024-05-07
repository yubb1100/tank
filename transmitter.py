import socket

import time
import pygame
import os
import pickle
import struct

class transmitter:
    def __init__(self):
        os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

        self.PORT2=5003
        self.HOST='142.232.234.243'
        
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')
        self.s2.bind((self.HOST, self.PORT2))
        print('socket binded')
        self.s2.listen(10)
        print('socket now listening')
        self.conn, self.addr = self.s2.accept()
        print('socket accepted, got connection object')

        pygame.init()
        pygame.joystick.init()
        print("Number of Joysticks: " + str(pygame.joystick.get_count()))
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.current = time.time()
        self.point = time.time()
        self.done = False
        #self.pi = ('142.232.234.239', 5003)
        

    def __del__(self):
        self.s2.close()
        
    def reset_time(self):
        self.point = time.time()
        self.current = time.time()

    def auto(self):
        self.reset_time()
        while (self.current - self.point) < 1:
            self.conn.sendall(str.encode("g w"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 0.25:
            self.conn.sendall(str.encode("g a"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 0.75:
            self.conn.sendall(str.encode("g p"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 0.60:
            self.conn.sendall(str.encode("g d"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 2.25:
            self.conn.sendall(str.encode("g p"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 0.5:
            self.conn.sendall(str.encode("g d"))
            self.current = time.time()
        self.reset_time()
        while (self.current - self.point) < 0.5:
            self.conn.sendall(str.encode("g p"))
            self.current = time.time()

    def run(self):
        while True:
            pygame.event.pump()
            if (self.current - self.point) > 0.02:
                self.x_l = self.joystick.get_axis(0)
                self.y_l = self.joystick.get_axis(1)
                self.x_r = self.joystick.get_axis(2)
                self.y_r = self.joystick.get_axis(3)
                self.t_l = self.joystick.get_axis(4)
                self.t_r = self.joystick.get_axis(5)
                self.dict = [
                    self.x_l,
                    self.y_l,
                    self.x_r,
                    self.y_r,
                    self.t_l,
                    self.t_r ]

            
                self.data = pickle.dumps(self.dict, 0)
                self.size = len(self.data)
                self.point = time.time()
                print("x_l: " + str(self.x_l) + " y_l: " + str(self.y_l))
            #print("{}: {}".format(self.img_counter, self.size))
                self.conn.sendall(struct.pack(">L", self.size) + self.data)
            #self.conn.send(self.msg)
            self.current = time.time()
            #print(self.msg)
            #if keyboard.is_pressed('q'):
            #    break
t1 = transmitter()
t1.run()
