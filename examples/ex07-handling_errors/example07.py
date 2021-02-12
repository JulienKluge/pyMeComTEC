#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from TEC_Serial import MeerstetterTEC_Serial
from TEC_Helper import MeParType, MeCom_DeviceStatus, MeComException
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = MeerstetterTEC_Serial(port = "COM10")

    #An error state is always indicated in the MeCom_DeviceStatus
    status = tec.status()
    if status == MeCom_DeviceStatus.Error:
        #Generally: if the TEC is in an error state, the get_error function can retreive all necessary information
        (err_number, err_instance, err_parameter, err_message) = tec.get_error()
        print("Error Nr. {} in instance {} (parameter {}): {}".format(err_number, err_instance, err_parameter, err_message))
        print("---")
    else:
        print("No Error")
    
    #If a request errors, then an exception (type: MeComException) will be raised
    try:
        #provoke an exception by raw reading a MeParID which does not exist
        tec.read_raw(999)
    except MeComException as e:
        print("MeCom Exception code {}: {}".format(e.mecom_error_number, e.mecom_error))
        print("---")

    #
    # To recover from a fail state, the tec can programmatically be reset
    tec.execute_reset()

    #wait for reset and read out status again
    time.sleep(5)
    status = tec.status()
    print(status)
    
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#Error Nr. 32 in instance 1 (parameter 4699): Power Supply Error:
#Internal Medium Voltage power net < Hard Limit
#---
#MeCom Exception code 5: MeComError.EER_PAR_NOT_AVAILABLE
#---
#MeCom_DeviceStatus.Run
#
