"""
Synthesizer
===========

A group of functions for synthesizing basic sounds with ndarrays

**Contents:**
- envelope: Returns an ndarray containing a linear ADSR envelope
- sine: Returns an ndarray containing a sine wave
- square: Returns an ndarray containing a square wave

**Usage:**
```python
from utils import synthesizer as synth
# or
import utils.synthesizer as synth
"""
import numpy as np

def envelope(attack: float,
             decay: float,
             sustain: float,
             release: float,
             sustain_len: float,
             samplerate: int) -> np.ndarray:
    """
    Returns an ndarray containing a linear ADSR envelope.
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
    ### Returns an ndarray containing a sine wave
    - 
    """
    t = np.linspace(0, samples / samplerate, samples, endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def square(frequency: float,
           samples: int,
           samplerate: int) -> np.ndarray:
    """
    ### Returns an ndarray containing a square wave
    """
    t = np.linspace(0, samples / samplerate, samples, endpoint=False)
    return np.sign(np.sin(2 * np.pi * frequency * t))