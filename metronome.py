import time

import sounddevice as sd
import numpy as np

class synthesize:
    """
    utilities for synthesizing metronome sounds
    """
    def envelope(attack: float,
                 decay: float,
                 sustain: float,
                 release: float,
                 sustain_len: float,
                 samplerate: int) -> np.ndarray:
        """
        returns an array representing a linear ADSR envelope
        - attack, decay, sustain_len, release should have units of seconds and values > 0
        - sustain should have value 0 <= x <= 1
        """
        a = np.arange(int(attack * samplerate)) / (attack * samplerate)
        d = 1 - np.arange(int(decay * samplerate)) * (1 - sustain) / (decay * samplerate)
        s = np.ones(int(sustain_len * samplerate)) * sustain
        r = sustain - np.arange(int(release * samplerate)) * sustain / (release * samplerate) if sustain > 0 else []
        return np.concatenate((a, d, s, r))

    def sine(frequency: float,
             samples: int,
             samplerate: int) -> np.ndarray:
        """
        returns an array representing a sine signal
        """
        t = np.linspace(0, samples / samplerate, samples, endpoint=False)
        return np.sin(2 * np.pi * frequency * t)

    def square(frequency: float,
               samples: int,
               samplerate: int) -> np.ndarray:
        """
        returns an array representing a square wave signal
        """
        t = np.linspace(0, samples / samplerate, samples, endpoint=False)
        return np.sign(np.sin(2 * np.pi * frequency * t))


def main():
    bpm = 120
    interval = 60 / bpm

    output_device_info = sd.query_devices(sd.default.device[1], 'output')
    #print(output_device_info)
    samplerate = output_device_info['default_samplerate']

    adsr = synthesize.envelope(0.01, 0.05, 0.4, 0.04, 0, samplerate)
    click = (synthesize.square(880, len(adsr), samplerate) * adsr).reshape(-1, 1)

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