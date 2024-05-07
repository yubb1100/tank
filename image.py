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

class image:
    def __init__(self):
        print(cv2.aruco.DICT_6X6_250)
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
        self.picam2.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.parameters = cv2.aruco.DetectorParameters_create()
        print("Aruco_dict: " + str(self.aruco_dict) + "\n")
        self.img_counter = 0

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('142.232.234.243', 4003))
        self.connection = self.client_socket.makefile('wb')

        #self.f = open("config.ini", "r")

        self.count = 0
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        #self.address = ('localhost', 6000)
        #self.listener = Listener(self.address, authkey=b'secret password')
        #self.conn = self.listener.accept()
        #print('connection accepted from', self.listener.last_accepted)

    def __del__(self):
        
        #self.f.close()
        self.client_socket.close()

    def run(self):
        while True:
            self.im = self.picam2.capture_array()
            self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
            self.corners, self.ids, self.rejected = cv2.aruco.detectMarkers(self.im, self.aruco_dict, parameters=self.parameters)
            if self.ids is not None:
                #print("entered if\n")
                cv2.aruco.drawDetectedMarkers(self.im, self.corners, self.ids)
            #self.face = self.face_classifier.detectMultiScale(self.im, scaleFactor=1.1, minNeighbors=5, minSize=(40,40))
           # for (x, y, w, h) in self.face:
           #     print("in loop")
           #     cv2.rectangle(self.im, (x, y), (x + w, y + h), (0, 255, 0), 4)

            self.nuImage = np.asarray(self.im[:,:])
            self.result, self.imgencode = cv2.imencode('.jpg', self.nuImage, self.encode_param)
            self.data = pickle.dumps(self.imgencode, 0)
            self.size = len(self.data)

            #print("{}: {}".format(self.img_counter, self.size))
            self.client_socket.sendall(struct.pack(">L", self.size) + self.data)
            self.img_counter += 1

            self.count = self.count + 1
            #self.msg = self.conn.recv()
            #if self.msg == 'close':
            #    self.conn.close()
            #    break
           # self.lines = self.f.readlines()
           #     if lines[1] == "1\n":
           #         break
           #     else:
           #         self.count = 0

i1 = image()
i1.run()
