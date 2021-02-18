from serial import Serial
from pyMeComTEC import TEC
from time import sleep

class TEC_Serial(TEC):
    """
    Discrete implementation of the TEC class on an USB based interface
    """
    def __init__(self, port, timeout = 1, baudrate = 57600, tec_address = 0, check_crc = True):
        super().__init__(
            tec_address = tec_address,
            check_crc = check_crc
        )

        self.port = port
        self.timeout = timeout
        self.baudrate = baudrate

        self.ser = Serial(
            port = self.port,
            timeout = self.timeout,
            baudrate = self.baudrate,
        )
        self.ser.flush()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.__exit__(exc_type, exc_val, exc_tb)

    def __enter__(self):
        return self

    def stop(self):
        self.ser.flush()
        self.ser.close()
    
    def _send_and_receive(self, frame):
        byte_arr = frame + b'\r'

        #clear all remaining buffers
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        
        #send and flush
        self.ser.write(byte_arr)
        self.ser.flush()

        #read all in
        answer_arr = self.ser.read_until(b'\r')
        return answer_arr[0:-1]
    
    def _send_and_ignore_receive(self, frame):
        byte_arr = frame + b'\r'

        #clear all remaining buffers
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        
        #send and flush
        self.ser.write(byte_arr)
        self.ser.flush()
        
        #wait for first answer and discard if tec_address is not 255
        if self.tec_address != 255:
            self.ser.read()
            self.ser.flush()
    
    def _speed_changed(self, speed):
        self.baudrate = speed
        self.ser.baudrate = speed

