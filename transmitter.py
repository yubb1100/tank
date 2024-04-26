import socket
import keyboard
import time

class transmitter:
    def __init__(self):
        self.PORT2=5003
        self.HOST='142.232.234.244'
    
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')
        self.s2.bind((self.HOST, self.PORT2))
        print('socket binded')
        self.s2.listen(10)
        print('socket now listening')
        self.conn, self.addr = self.s2.accept()
        print('socket accepted, got connection object')

    def __del__(self):
        self.s2.close()

    def run(self):
        while True:
            if keyboard.is_pressed('w'):
                self.conn.sendall(str.encode("g w"))
                print('w')
            elif keyboard.is_pressed('a'):
                self.conn.sendall(str.encode("g a"))
                print('a')
            elif keyboard.is_pressed('s'):
                self.conn.sendall(str.encode("g s"))
                print('s')
            elif keyboard.is_pressed('d'):
                self.conn.sendall(str.encode("g d"))
                print('d')
            elif keyboard.is_pressed('p'):
                self.conn.sendall(str.encode("g p"))
                print('p')
            elif keyboard.is_pressed('l'):
                self.conn.sendall(str.encode("g l"))
                print("l")
            elif keyboard.is_pressed('j'):
                self.conn.sendall(str.encode("g j"))
                print("j")
            elif keyboard.is_pressed('q'):
                self.conn.sendall(str.encode("g q"))
                print("q")
                break
            else:
                self.conn.sendall(str.encode("g N"))

t1 = transmitter()
t1.run()
