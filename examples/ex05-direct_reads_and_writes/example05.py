#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from TEC_Serial import MeerstetterTEC_Serial
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = MeerstetterTEC_Serial(port = "COM10")

    #
    # The tec object only provides convenience functions for commonly used values
    # For all other values, there is a raw function implemented by a name in the
    # shape of:
    # (Get|Set)_PREFIX_ValueName
    # As an example, lets look at the measured temperature:
    #
    # Get_TEC_ObjectTemperature
    #
    # Get|Set: Get
    # Prefix:  TEC
    # Name:    ObjectTemperature
    #
    # All those functions are implemented in src/TEC_autogen for reference.
    # The convenience functions are then just wrappers around those raw functions
    #

    #
    # For example:
    # the current_limit convenience function just wraps Get_TEC_CurrentLimitation
    # so we expect the same value from both calls:
    print("{} == {} ?".format(tec.current_limit(), tec.Get_TEC_CurrentLimitation()))

    #
    # Lets read the sink temperature anf fan speed in this way:
    print("Sink temperature: {} °C".format(tec.Get_TEC_SinkTemperature()))
    print("Fan Speed: {} RPM".format(tec.Get_TEC_FanActualFanSpeed()))

    #
    # Write the current output limit via the convenience function and its direct function
    tec.write_current_limit(2.1)
    tec.Set_TEC_CurrentLimitation(2.2)
    
    
    #
    # A write to the tec usually waits for an answer to verify it was received and executed properly.
    # If there is no need to do that, use the fire_and_forget option to discard any answers
    # This is commonly used in situations were multiple TECs are on the same bus and the broadcast address is used
    tec.Set_TEC_CurrentLimitation(2.0, fire_and_forget = True)
    print(tec.current_limit())


    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#2.0 == 2.0 ?
#Sink temperature: 25.0 °C
#Fan Speed: 0.0 RPM
#
