#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
from pyMeComTEC_Helper import MeParType
import time, math

#
# unfinished
#

def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    with open("tec_settings_dump.csv", "w") as f:
        for p in tec.TEC_PARAMETERS:
            p_id = p["id"]
            p_name = p["name"]
            p_type = p["mepar_type"]
            if p_id >= 50000:
                continue
            try:
                metadata = tec.read_metadata(p_id)
            except:
                continue
            (r_mepar_type, r_mepar_flag, _, _, _, _, _) = metadata
            if not r_mepar_flag.is_readwrite():
                continue
            if (r_mepar_type != p_type):
                print(f"!!!MISTYPED!!! {p_name} {r_mepar_type.get_type()} vs {p_type.get_type()}")
                continue
            p_set_value = tec._read_value(p_id, p_type)
            if not math.isnan(p_set_value):
                if p_set_value > 2147483646 or p_set_value < -2147483646:
                    print(f"!!!OUT OF BOUNDS!!! {p_name},{p_set_value}")
                else:
                    f.write(f"{p_name},{p_id},{p_type},{p_set_value}\n")
                #print(f"{p_name},{p_set_value}")
            else:
                print(f"!!!NAN!!! {p_name}")
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#

#
