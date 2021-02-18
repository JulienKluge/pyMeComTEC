#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
import time


def main():
    
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    #read current temperature and temperature target
    print("Temperature: {} °C".format(tec.temperature()))
    print("Target Temperature: {} °C".format(tec.target_temperature()))

    #change temperature target and wait for 10s
    print("Changing temperature target to 30°C and wait for 10s")
    tec.write_target_temperature(30.0)
    time.sleep(10.0)

    #read current temperature
    print("Temperature: {} °C".format(tec.temperature()))
    print("Target Temperature: {} °C".format(tec.target_temperature()))
    if tec.temperature_is_stable():
        print("Temperature is stable.")
    else:
        print("Temperature is NOT stable!")

    #reset temperature
    print("Reset temperature to 26°C")
    tec.write_target_temperature(26.0)
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Temperature: 26.00048828125 °C
#Target Temperature: 26.0 °C
#Changing temperature target to 30°C and wait for 10s
#Temperature: 29.428680419921875 °C
#Target Temperature: 30.0 °C
#Temperature is NOT stable!
#Reset temperature to 26°C
#
