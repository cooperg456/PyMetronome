import threading
import time

import sounddevice as sd
import numpy as np


bpm = 400
interval = 60 / bpm

frequency = 440
duration = 0.05
fs = 48000

def main():
    start_idx = 0
    frequency = 440
    amplitude = 0
    amp_lock = threading.Lock()

    output_device_info = sd.query_devices(sd.default.device[1], 'output')
    #print(output_device_info)
    samplerate = output_device_info['default_samplerate']

    def callback(outdata, frames, time_data, status):
        if status:
            print(status)
        with amp_lock:
            volume = amplitude
        nonlocal start_idx
        t = (start_idx + np.arange(frames)) / samplerate
        t = t.reshape(-1, 1)
        outdata[:] = volume * np.sin(2 * np.pi * frequency * t)
        start_idx += frames

    O_STREAM = sd.OutputStream(device=sd.default.device[1],
                               channels=1,
                               dtype='float32',
                               latency='low',
                               callback=callback,
                               samplerate=samplerate,)

    O_STREAM.start()
    STARTUP_TIME = time.perf_counter()
    while True:
        with amp_lock:
            amplitude = 1
        time.sleep(0.05)
        with amp_lock:
            amplitude = 0

        # hybrid waiting to quantize each beat
        sleep_time = interval - (time.perf_counter() - STARTUP_TIME) % interval - 0.005
        if sleep_time > 0:
            time.sleep(sleep_time)
        while (time.perf_counter() - STARTUP_TIME) % interval > 0.0001:
            pass


if __name__ == "__main__":
    main()