import socket
from pyMeComTEC import TEC
from time import sleep

class TEC_TCP(TEC):
    """
    Discrete implementation of the TEC class on a TCP-socket based interface
    """
    def __init__(self, address, port = 50000, timeout = 1, tec_address = 0, check_crc = True):
        super().__init__(
            tec_address = tec_address,
            check_crc = check_crc
        )

        self.timeout = timeout
        self.address = address
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((address, port))
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.close()

    def __enter__(self):
        return self

    def stop(self):
        self.s.close()
    
    def _send_and_receive(self, frame):
        byte_arr = frame + b'\r'
        self.s.send(byte_arr)

        answer = self.s.recv(256)
        if len(answer) < 2:
            raise Exception("TCP interface received empty response")
        if answer[-1] == 13: #13=b'\r'
            answer = answer[0:-1]
        return answer
    
    def _send_and_ignore_receive(self, frame):
        byte_arr = frame + b'\r'
        self.s.send(byte_arr)

        if self.tec_address != 255:
            self.s.recv(256)
    
    def _speed_changed(self, speed):
        raise Exception("Speed Change is not supported on the default TCP interface")

