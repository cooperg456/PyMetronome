import sounddevice as sd
import numpy as np
import time

bpm = 120
interval = 60 / bpm

frequency = 440
duration = 0.05
fs = 48000

t = np.linspace(0, duration, int(fs * duration), endpoint=False)

sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

def main():
    STARTUP_TIME = time.perf_counter()
    
    while True:
        sd.play(sine_wave, fs)

        # hybrid waiting to quantize each beat
        sleep_time = interval - (time.perf_counter() - STARTUP_TIME) % interval - 0.005
        if sleep_time > 0:
            time.sleep(sleep_time)
        while (time.perf_counter() - STARTUP_TIME) % interval > 0.0001:
            pass

if __name__ == "__main__":
    main()