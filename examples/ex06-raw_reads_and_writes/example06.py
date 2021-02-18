#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
from pyMeComTEC_Helper import MeParType
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    #
    # The tec object implements all publicly known and available in/outs of the TEC
    # These properties are identified by a number called MeParID
    # Sometimes one might want to these ID's directly instead of the convenience functions, or direct calls
    # as well as interpreting the raw answers to that.
    # For those tasks, the tec object proved the read_raw and write_raw functions

    #
    # The actual temperature is known under the MeParID=1000
    # Lets read it out with the three known methods:
    print("Temperature (Convenience Function): {} °C".format(tec.temperature()))
    print("Temperature (Direct Function): {} °C".format(tec.Get_TEC_ObjectTemperature()))
    print("Temperature (Raw Function): {} °C".format(tec.read_raw(1000)))

    #As one can see however, the read_raw call returned a byte array instead.
    #It has to be interpreted as a float to be valid.
    #The TEC_Helper includes the MeParType class to do exactly that:
    raw_response = tec.read_raw(1000)
    interpreted_response = MeParType.FLOAT32.interpret_type(raw_response)
    print("---")
    print("Raw: {} --> Interpreted: {}".format(raw_response, interpreted_response))

    #
    # Also, the TEC class inherits a TEC_PARAMETERS array, which includes information about every known MeParID
    # Lets find the info about the MeParID=1050 for example:
    for d in tec.TEC_PARAMETERS:
        if d["id"] == 1050:
            print(d)
            break

    #
    # This can also be automated by the find_meparid function which takes in the meparid OR the name string
    print("---")
    print(tec.find_meparid(1010))
    print("---")
    print(tec.find_meparid("SinkTemperature"))

    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Temperature (Convenience Function): 26.00067138671875 °C
#Temperature (Direct Function): 26.001068115234375 °C
#Temperature (Raw Function): b'41D00230' °C
#---
#Raw: b'41D00230' --> Interpreted: 26.001068115234375
#{'prefix': 'TEC', 'id': 1050, 'name': 'FirmwareVersion', 'type': <class 'int'>, 'mepar_type': <MeParType.INT32: 1>, 'readonly': True}
#---
#{'prefix': 'TEC', 'id': 1010, 'name': 'TargetObjectTemperature', 'type': <class 'float'>, 'mepar_type': <MeParType.FLOAT32: 0>, 'readonly': True}
#---
#{'prefix': 'TEC', 'id': 1001, 'name': 'SinkTemperature', 'type': <class 'float'>, 'mepar_type': <MeParType.FLOAT32: 0>, 'readonly': True}
#
