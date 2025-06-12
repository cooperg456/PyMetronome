"""
textinterface
=============

A group of functions for creating text interfaces 
(Many functions depend on the value of os.name. The program will run sys.exit(1) in the event of an unsupported os)

**Compatability**
- POSIX (mac, linux): ?
- NT (windows): In progress
- JAVA (JPython): Unsupported

**Contents:**
- splashScreen: Generates PyMetronome splash screen with auxilary text

**Usage:**
```python
from utils import textinterface as ti
# or
import utils.textinterface as ti
"""
import os
import sys
import datetime


match os.name:
    case 'posix':
        import tty
        import termios


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

    case 'nt':
        import msvcrt


        def getch() -> str:
            """
            Blocks input, waits for keypress and returns its value
            Catches Ctrl+C and raises KeyboardInterrupt
            """
            ch = msvcrt.getch()
            if ch == b'\x03': # Ctrl+C
                raise KeyboardInterrupt
            return ch

    case _:
        raise NotImplementedError(f"Unsupported system: os.name='{os.name}'")


def splashScreen(aux: str = None) -> str:
    """
    Generates PyMetronome splash screen with auxilary text
    """
    clr = "\033[0m"
    if datetime.datetime.now().month == 6:
        yel = "\033[38;2;255;237;0m"
        pur = "\033[38;2;107;35;141m"
        wht = "\033[38;2;255;255;255m"
        pnk = "\033[38;2;245;169;184m"
        lbl = "\033[38;2;91;206;250m"
        bro = "\033[38;2;101;57;49m"
        red = "\033[38;2;224;0;0m"
        org = "\033[38;2;255;121;0m"
        grn = "\033[38;2;0;135;62m"
        blu = "\033[38;2;0;82;165m"
    else:
        yel = pur = wht = pnk = lbl = bro = red = org = grn = blu = clr

    auxText = f"\033[2;3m{aux}"

    splashText = rf"""    {yel}____        {pnk}__  ___     {bro}__{clr}
   {yel}/ {pur}__ {yel}\{wht}__  __{pnk}/  |/  /{lbl}__  {bro}/ /_{red}_____{org}____  {yel}____  {grn}____  {blu}____ ___  {pur}___{clr}
  {yel}/ {pur}/_/ {wht}/ / / {pnk}/ /|_/ {lbl}/ _ \{bro}/ __{red}/ ___{org}/ __ \{yel}/ __ \{grn}/ __ \{blu}/ __ `__ \{pur}/ _ \{clr}
 {yel}/ ____{wht}/ /_/ {pnk}/ /  / {lbl}/  __{bro}/ /_{red}/ /  {org}/ /_/ {yel}/ / / {grn}/ /_/ {blu}/ / / / / {pur}/  __/{clr}
{yel}/_/    {wht}\__, {pnk}/_/  /_/{lbl}\___/{bro}\__{red}/_/   {org}\____{yel}/_/ /_/{grn}\____{blu}/_/ /_/ /_/{pur}\___/{clr}
      {wht}/____/{clr}                                                           
"""
    return splashText[:-len(auxText)] + auxText + "\033[0m\n" if aux is not None else splashText

def mainMenu(bpm: int,
             ts: str,
             run: bool,
             refresh=False) -> str:
    state = "RUN" if not run else "STOP"
    menuText = "+" + "-" * 66 + "+\n" + "|  " + f"(SPACE) {state:>4} | (↑↓) BPM : {bpm:>3} | (←→) TS : {ts:>4} | (CTRL+C) QUIT" + "  |\n" + "+" + "-" * 66 + "+\n"
    refreshText = "\r" + "\033[3A"
    return refreshText + menuText if refresh else menuText