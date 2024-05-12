from picamera2 import Picamera2
import numpy as np
import cv2
import io
import pickle
import time
import zlib
import socket
import struct

import subprocess

import sys

from multiprocessing.connection import Listener

import board
import busio
import adafruit_vl53l0x

class image:
    def __init__(self):
        print(cv2.aruco.DICT_6X6_250)
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
        self.picam2.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        
        self.img_counter = 0

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('142.232.234.243', 4003))
        self.connection = self.client_socket.makefile('wb')

        self.count = 0
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)

    def __del__(self):
        
        #self.f.close()
        self.client_socket.close()

    def run(self):
        while True:
            try:
                self.im = self.picam2.capture_array()
                #self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)

                self.nuImage = np.asarray(self.im[:,:])
                self.result, self.imgencode = cv2.imencode('.jpg', self.nuImage, self.encode_param)
                self.data = pickle.dumps(self.imgencode, 0)
                self.size = len(self.data)
                self.num_bytes = struct.pack(">I", self.sensor.range)
                self.client_socket.sendall(struct.pack(">L", self.size) + self.num_bytes + self.data)                
            except:
                pass    
            
            

i1 = image()
i1.run()
