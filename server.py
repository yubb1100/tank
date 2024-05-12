from multiprocessing import Process, Pipe

import receiver
import transmitter

def tx(pipe):
    t = transmitter.transmitter()
    t.run(pipe)
def rx(pipe):
    r = receiver.receiver()
    r.run(pipe)
    
def main():
    parent_conn, child_conn = Pipe()
    
    tx_process = Process(target=tx, args=(child_conn,))
    rx_process = Process(target=rx, args=(parent_conn,))

    tx_process.start()
    rx_process.start()

    tx_process.join()
    rx_process.join()

    print("Both scripts have finished executing.")

if __name__ == '__main__':
    main()
