#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
from pyMeComTEC import MeCom_DeviceStatus
import time
from random import uniform

import matplotlib.pyplot as plt
from scipy.signal import welch, csd
from math import pi


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")
    print(tec.read_firmware_id())

    #check if TEC is running
    if tec.status() != MeCom_DeviceStatus.Run:
        print("TEC is not running")
        return
    
    #temp the tec started out with
    starting_temp = tec.target_temperature()

    #perform the measurement run
    ramp_max_delta = 2.0   # maximunm temperature deviation to set
    ramp_min_delta = 0.1   # minimum temperature deviation to set
    ramp_max_time = 120.0   # maximum time for each ramp
    ramp_min_time = 30.0    # minimum time for each ramp
    ramps_n = 2           # perform 20 runs
    measurement_time = 0.2 # minimum time between measurements
    (times, setpoints, temps) = tec_perform_response_curves(
        tec,
        starting_temp,
        ramp_max_delta,
        ramp_min_delta,
        ramp_max_time,
        ramp_min_time,
        ramps_n,
        measurement_time
    )

    #reset to starting temperature
    tec.write_target_temperature(starting_temp)

    #transfer function estimation
    rate = len(times) / (times[-1] - times[1])
    _, pxy = csd(setpoints, temps, fs = rate, window = 'hann', nperseg = 512)
    pxx_f, pxx = welch(setpoints, fs = rate, window = 'hann', nperseg = 512)
    tfe_abs = [abs(xy / xx) for xy, xx in zip(pxy, pxx)]
    tfe_arg = [180.0 / pi * (xy / xx).imag for xy, xx in zip(pxy, pxx)]


    #plot results
    fig, axs = plt.subplots(2)
    axs[0].loglog(pxx_f, tfe_abs)
    axs[0].set(xlabel='Time t / s', ylabel='Temperature T / °C')
    axs[1].semilogx(pxx_f, tfe_arg)
    axs[1].set(xlabel='Time t / s', ylabel='Phase phi / °')
    plt.show()

    
def tec_perform_response_curves(tec, T0, max_delta, min_delta, max_time, min_time, runs, min_wait_time):
    times = []
    setpoints = []
    measurements = []

    starting_time = time.time()

    run_idx = 0
    current_temp = T0
    first_state = True
    state_time = time.time()
    state_time_projected = max_time

    while run_idx < runs:
        time.sleep(min_wait_time)
        duration = time.time() - starting_time
        temp = tec.temperature()

        times += [duration]
        setpoints += [current_temp]
        measurements += [temp]

        print("Run {} / {}  {:<19} / {}°C".format(
            run_idx,
            runs,
            temp,
            current_temp
        ))

        state_duration = time.time() - state_time
        if state_duration > state_time_projected:
            state_time = time.time()
            if first_state:
                first_state = False
                current_temp = uniform(min_delta, max_delta) + T0
                tec.write_target_temperature(current_temp)
            else:
                first_state = True
                current_temp = T0
                tec.write_target_temperature(current_temp)
                run_idx += 1
            state_time_projected = uniform(min_time, max_time)

    return (times, setpoints, measurements)


if __name__ == '__main__':
    main()
