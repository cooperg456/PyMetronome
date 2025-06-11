import time

import sounddevice as sd
import numpy as np

import utils.synthesizer as synth


def main():
    bpm = 120
    interval = 60 / bpm

    output_device_info = sd.query_devices(sd.default.device[1], 'output')
    #print(output_device_info)
    samplerate = output_device_info['default_samplerate']

    adsr = synth.envelope(0.01, 0.05, 0.4, 0.04, 0, samplerate)
    click = (synth.square(880, len(adsr), samplerate) * adsr).reshape(-1, 1)

    sound_idx = 0
    sound_len = len(click) # precompute
    next_click = time.perf_counter()
    def callback(outdata, frames, time_data, status):
        nonlocal sound_idx
        nonlocal next_click
        if status:
            print(status)
        if time.perf_counter() >= next_click:
            sound_idx = 0
            next_click += interval
        outdata[:] = 0
        if sound_idx <= len(click):
            write_len = np.min((frames, sound_len - sound_idx))
            outdata[:write_len] = click[sound_idx:sound_idx+write_len]
            sound_idx += write_len

    with sd.OutputStream(device=sd.default.device[1],
                         channels=1,
                         dtype='float32',
                         latency='low',
                         callback=callback,
                         samplerate=samplerate,) as stream:
        while True:
            time.sleep(1) # prevent cpu spinning that leads to output underflow in callback


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interupted by user")