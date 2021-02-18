#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial


def main():
    
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    #
    # The usual tec object provides for some convenience functions
    # to read out temperature, voltage, currents and their targets/limits
    #
    print("Temperature: {} °C".format(tec.temperature()))
    print("Output Current: {} A".format(tec.current()))
    print("Output Voltage: {} V".format(tec.voltage()))

    print("---")

    print("Target Temperature: {} °C".format(tec.target_temperature()))
    print("Current Limit: {} A".format(tec.current_limit()))
    print("Current Error Threshold: {} A".format(tec.current_error_threshold()))
    print("Voltage Limit: {} V".format(tec.voltage_limit()))
    print("Voltage Error Threshold: {} V".format(tec.voltage_error_threshold()))

    print("---")

    #
    # Check if temperature is stable
    #
    if tec.temperature_is_stable():
        print("Temperature is stable.")
    else:
        print("Temperature is NOT stable!")
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Temperature: 25.99993896484375 °C
#Output Current: 0.11978787183761597 A
#Output Voltage: 0.6997480392456055 V
#---
#Target Temperature: 26.0 °C
#Current Limit: 2.0 A
#Current Error Threshold: 4.0 A
#Voltage Limit: 10.0 V
#Voltage Error Threshold: 20.0 V
#---
#Temperature is stable.
#
