#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_TCP import TEC_TCP


def main():
    
    #allocate the tec object for a tcp-socket connection at an ip address 192.168.0.6
    #(can be a hostname too) within the standard port 50000
    tec = TEC_TCP(address = "192.168.0.6")

    #read the firmware id
    print("Firmware ID: {}".format(tec.read_firmware_id()))

    #read the tec hardware
    print("Device Type: {}".format(tec.Get_COM_DeviceType()))
    print("Hardware Version: {}".format(tec.Get_COM_HardwareVersion()))
    print("Serial Number: {}".format(tec.Get_COM_SerialNumber()))

    #read the tec status
    print(tec.status())


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Firmware ID: 8065-TEC SW G01
#Device Type: 1091
#Hardware Version: 180
#Serial Number: 3941
#MeCom_DeviceStatus.Run
#
