from serial import Serial
from TEC import MeerstetterTEC

class MeerstetterTEC_USB(MeerstetterTEC):
    """
    Discrete implementation of the MeerstetterTEC class on an USB based interface
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
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.__exit__(exc_type, exc_val, exc_tb)

    def __enter__(self):
        return self

    def stop(self):
        self.ser.flush()
        self.ser.close()
    
    def _sendAndReceive(self, frame):
        byte_arr = frame + b'\r'

        #clear all remaining buffers
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        
        #send and flush
        self.ser.write(byte_arr)
        self.ser.flush()

        #read all in
        answer_arr = self.ser.read_until(terminator = b'\r')
        return answer_arr[0:-1]


