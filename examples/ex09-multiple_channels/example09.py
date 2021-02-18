#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    # By default, all functions will read/write to channel 1
    # This can always be changed by using the channel option:
    print("Temperature Ch1: {}".format(tec.temperature(channel = 1)))
    print("Temperature Ch2: {}".format(tec.temperature(channel = 2)))

    #
    # Also, both channels can be read sequentially too:
    print(tec.temperature(channel= [1, 2]))
    #reading these simultaneously requires bulk reads (example 10)

    #
    # This also works for direkt functions as well as raw functions reads/writes
    tec.Set_TEC_CurrentLimitation(2.0, channel=[1, 2])
    print(tec.read_raw(1010, channel = 2))
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Temperature Ch1: 26.00042724609375
#Temperature Ch2: nan
#[26.00042724609375, nan]
#b'00000000'
#
