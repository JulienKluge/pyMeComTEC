#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
from pyMeComTEC import MeCom_DeviceStatus
import time

import matplotlib.pyplot as plt


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")
    print(tec.read_firmware_id())

    #check if TEC is running
    if tec.status() != MeCom_DeviceStatus.Run:
        print("TEC is not running")
        return
    
    #set tec stability indicator maximum temp. deviation
    tec.Set_TEC_StabilityTemperatureWindow(0.01)
    
    #read in table file
    table = [ 26.0 ]
    with open("sin_table.csv", "r") as filestream:
        for line in filestream:
            table += [float(line)]
    
    #perform software lookup table
    wait_for_stabilization = True #wait at each step for temperature stabilization
    min_wait_time = 1.0 #seconds
    print_progress = True
    (times, temps, setpoints) = tec_perform_lookup(
        tec,
        table,
        wait_for_stabilization,
        min_wait_time,
        print_progress
    )

    #plot results
    plt.plot(times, temps, label = 'Temperature')
    plt.plot(times, setpoints, label = 'Set Point')
    plt.legend(loc = "upper left")
    plt.xlabel("Time t / s")
    plt.ylabel("Temperature T / °C")
    plt.show()

    
def tec_perform_lookup(tec, table, wait_for_stabilization, min_wait_time, print_progress):
    start_time = time.time()

    measurements = []
    measurement_soll = []
    measurement_times = []

    for idx, t_entry in enumerate(table):
        meas = tec.temperature()
        measurements += [meas]

        duration = time.time() - start_time
        measurement_soll += [t_entry]
        measurement_times += [duration]

        tec.write_target_temperature(t_entry)

        if print_progress:
            print("Entry {}/{}: {}/{} °C ({}s)".format(
                idx + 1,
                len(table),
                meas,
                t_entry,
                duration
            ))

        time.sleep(min_wait_time)

        if wait_for_stabilization:
            while not tec.temperature_is_stable():
                measurements += [tec.temperature()]
                measurement_soll += [t_entry]
                measurement_times += [time.time() - start_time]

                time.sleep(min_wait_time)
    
    return (measurement_times, measurements, measurement_soll)


if __name__ == '__main__':
    main()
