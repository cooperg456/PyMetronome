import os
import sys

from utils import textinterface as ti


def main():
    run = False
    bpm = 120
    tsi = 0 # time signiture index
    ts = ["4/4", "7/8"]

    sys.stdout.write(ti.splashScreen(f"sys:{os.name}, v:pre-alpha"))
    sys.stdout.write(ti.mainMenu(bpm, ts[tsi], run))

    try:
        while True:
            match ti.getch():
                case b' ':
                    run = not run
                case b'\xe0':
                    match ti.getch():
                        case b'H': # up
                            bpm += 5
                            bpm = max(40, min(bpm, 400))
                        case b'P': # down
                            bpm -= 5
                            bpm = max(40, min(bpm, 400))
                        case b'K': # left
                            tsi += 1
                            tsi %= len(ts)
                        case b'M': # right
                            tsi -= 1
                            tsi %= len(ts)

            sys.stdout.write(ti.mainMenu(bpm, ts[tsi], run, refresh=True))

    except KeyboardInterrupt:
        sys.stdout.write("Exiting on Ctrl+C")
        sys.exit(0)
        

if __name__ == "__main__":
    main()