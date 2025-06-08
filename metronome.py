from playsound3 import playsound
import time

bpm = 120
interval = 60 / bpm

def main():
    STARTUP_TIME = time.perf_counter()
    
    while True:
        playsound("808cb.wav", block=False)

        # hybrid waiting to quantize each beat
        sleep_time = interval - (time.perf_counter() - STARTUP_TIME) % interval - 0.005
        if sleep_time > 0:
            time.sleep(sleep_time)
        while (time.perf_counter() - STARTUP_TIME) % interval > 0.0001:
            pass

if __name__ == "__main__":
    main()