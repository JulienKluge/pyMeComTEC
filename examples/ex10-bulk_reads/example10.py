#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    #
    # Bulk reads allow for reading multiple properties on multiple channels at once

    #
    #read both temperature channels at once:
    print(tec.read_bulk(1000, channels = [1, 2]))

    #
    #read the temperature and target temperature at channel 1 at once
    print(tec.read_bulk([1000, 1010]))

    
    #
    #One can specify the properties via their direct MeParID or their name:
    print(tec.read_bulk([1000, "TargetObjectTemperature"], channels = 1))

    #
    #If both arguments are in vector form, then every parameter entry is read at the respective defined channel
    #Read temperature in channel 1, voltage in channel 2, and current in channel 1
    print(tec.read_bulk(["ObjectTemperature", "ActualOutputVoltage", "ActualOutputCurrent"], channels = [1, 2, 1]))

    #
    #Read the complete Hardware/Software identification
    print("---")
    read_str = ["DeviceType", "HardwareVersion", "SerialNumber", "FirmwareVersion", "DeviceStatus"]
    answer = tec.read_bulk(read_str)
    for rs, a in zip(read_str, answer):
        print("{}: {}".format(rs, a))
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#[25.999725341796875, nan]
#[25.999725341796875, 26.0]
#[25.99969482421875, 26.0]
#[25.99969482421875, 0.0, 0.11607012152671814]
#---
#DeviceType: 1091
#HardwareVersion: 180
#SerialNumber: 3941
#FirmwareVersion: 410
#DeviceStatus: 2
#
