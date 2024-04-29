#from picamera2 import Picamera2
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

class image:
    def __init__(self):
        print(cv2.aruco.DICT_6X6_250)
        self.cap =cv2.VideoCapture('udpsrc port=5200 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

        if self.cap.isOpened() is not True:
            print("Cannot open camera")
        #self.picam2 = Picamera2()
        #self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
        #self.picam2.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.parameters = cv2.aruco.DetectorParameters_create()
        print("Aruco_dict: " + str(self.aruco_dict) + "\n")
        self.img_counter = 0

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('142.232.234.244', 4003))
        self.connection = self.client_socket.makefile('wb')

        #self.f = open("config.ini", "r")

        self.count = 0
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    def __del__(self):
        
        #self.f.close()
        self.client_socket.close()

    def run(self):
        while True:
            self.im = self.cap.read()
#self.im = self.picam2.capture_array()
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

           # self.lines = self.f.readlines()
           #     if lines[1] == "1\n":
           #         break
           #     else:
           #         self.count = 0

i1 = image()
i1.run()
