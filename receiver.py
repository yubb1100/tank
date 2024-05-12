import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
from multiprocessing import Pipe

class receiver:
    def __init__(self):
        self.HOST='142.232.234.243'
        self.PORT=4003
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(10)
        self.conn, self.addr = self.s.accept()

        self.data = b""

        self.payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(self.payload_size))

        self.flag = 0
        self.count = 0

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        self.flag = 1
        cv2.namedWindow("ImageWindow", cv2.WINDOW_AUTOSIZE)
        self.face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def __del__(self):
        self.s.close()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self, pipe):
        while cv2.getWindowProperty('ImageWindow', 0) >= 0 or self.flag == 1:
            #pipe.send("blah")
            print("plop")
            while len(self.data) < self.payload_size + 4:
                #print("Recv: {}".format(len(data)))
                self.data += self.conn.recv(4096)
                #print("Done Recv: {}".format(len(data)))
            self.packed_msg_size = self.data[:self.payload_size]
            self.packed_number = self.data[self.payload_size:self.payload_size + 4]
            self.data = self.data[self.payload_size + 4:]
            self.msg_size = struct.unpack(">L", self.packed_msg_size)[0]
            self.number = int.from_bytes(self.packed_number, byteorder='big')
            print(self.number)
            #print("msg_size: {}".format(msg_size))
            while len(self.data) < self.msg_size:
                self.data += self.conn.recv(4096)
            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]

            self.frame=pickle.loads(self.frame_data, fix_imports=True, encoding="bytes")
            self.frame = cv2.imdecode(self.frame, -1)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            self.corners, self.ids, self.rejected = cv2.aruco.detectMarkers(self.gray, self.aruco_dict, parameters=self.parameters)
            if self.ids is not None:
                #print("entered if\n")
                cv2.aruco.drawDetectedMarkers(self.frame, self.corners, self.ids)
            self.face = self.face_classifier.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
            if len(self.face) != 0:
                for (x, y, w, h) in self.face:
                    pipe.send("pew " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            else:
                pipe.send("blah")
            cv2.imshow('ImageWindow',self.frame)
            self.flag = 0
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.i = 0
                while self.i < 10:
                    pipe.send("quit")
                    self.i = self.i + 1
                break
            #print(pipe.recv())
        pipe.send("quit")        


#r1 = receiver()
#r1.run()
