import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

class receiver:
    def __init__(self):
        self.HOST='142.232.234.244'
        self.PORT=4003
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(10)
        self.conn, self.addr = self.s.accept()

        self.data = b""

        self.payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(self.payload_size))

    def __del__(self):
        self.s.close()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self):
        while True:
            print("plop")
            while len(self.data) < self.payload_size:
                #print("Recv: {}".format(len(data)))
                self.data += self.conn.recv(4096)
                #print("Done Recv: {}".format(len(data)))
            self.packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack(">L", self.packed_msg_size)[0]
            #print("msg_size: {}".format(msg_size))
            while len(self.data) < self.msg_size:
                self.data += self.conn.recv(4096)
            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]

            self.frame=pickle.loads(self.frame_data, fix_imports=True, encoding="bytes")
            self.frame = cv2.imdecode(self.frame, cv2.IMREAD_COLOR)
            cv2.imshow('ImageWindow',self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


r1 = receiver()
r1.run()
