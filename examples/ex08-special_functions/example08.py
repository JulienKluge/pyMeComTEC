#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from TEC_Serial import MeerstetterTEC_Serial
from TEC_Helper import MeParType
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = MeerstetterTEC_Serial(port = "COM10")

    # Special functions are all designated by using an non VR, VS frame for sending and usually serve a special purpose
    # Those are:

    #firmware id read
    print(tec.read_firmware_id())

    #metadata read (read the metadata for a given MeParID)
    #(mepar_type, mepar_flag, instance_nr, max_nr, min_value, max_value, act_value)
    print(tec.read_metadata(1010))

    #big value reads (the default display text in this case)
    print(tec.read_big_value(6024, MeParType.LATIN1, 1))

    #bulk value reads
    print(tec.read_bulk([100, 101, 102, 103, 104]))

    # All execute_* functions:
    tec.execute_emergency_stop() #stops the tec, goes into an error state with MeComError.ERR_CUSTOM_EMERGENCY_STOP
    tec.execute_reset() #resets the tec
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#8065-TEC SW G01
#(<MeParType.FLOAT32: 0>, <TEC_Helper.MeParFlags object at 0x0000024E44F0B508>, 2, 1, -inf, inf, 26.0)
#T = {1000;1;5;8}°C
#[1091, 180, 3941, 410, 2]
#
