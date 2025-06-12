"""
textinterface
=============

A group of functions for creating text interfaces 
(Many functions depend on the value of os.name. The program will run sys.exit(1) in the event of an unsupported os)

**Compatability**
- POSIX (mac, linux): Full compatability
- NT (windows): Coming soon
- JAVA (JPython): Unsupported

**Contents:**
- splashScreen: Generates PyMetronome splash screen with auxilary text

**Usage:**
```python
from utils import textinterface as tui
# or
import utils.textinterface as tui
"""
import os
import sys


match os.name:
    case 'posix':
        import tty
        import termios


        def disableEcho():
            fd = sys.stdin.fileno()
            attrs = termios.tcgetattr(fd)
            attrs[3] &= ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSADRAIN, attrs)

        def getch() -> str:
            """
            Blocks input, waits for keypress and returns its value
            """
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    case 'nt' | 'java':
        raise NotImplementedError(f"Unsupported system: os.name='{os.name}'")


def splashScreen(aux: str = None) -> str:
    """
    Generates PyMetronome splash screen with auxilary text
    """
    auxText = f"|\033[2;3m{aux}"
    splashText = f"""\033[31m
===================================================
 _____     _____     _                             
|  _  |_ _|     |___| |_ ___ ___ ___ ___ _____ ___ 
|   __| | | | | | -_|  _|  _| . |   | . |     | -_|
|__|  |_  |_|_|_|___|_| |_| |___|_|_|___|_|_|_|___|
      |___|                                        
===================================================
"""
    return splashText[:5-len(auxText)] + auxText + "\033[0m\n" if aux is not None else splashText