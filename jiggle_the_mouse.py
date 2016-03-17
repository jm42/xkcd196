#!/usr/bin/env python

import argparse
import time
import sys


if sys.platform == 'darwin':
    raise NotImplementedError('MacOS is not yet supported')
elif sys.platform == 'win32':
    raise NotImplementedError('Windows is not yet supported')
else:
    from Xlib import X
    from Xlib.display import Display
    from Xlib.ext.xtest import fake_input

    display = Display(None)

    def get_mouse_pos():
        pointer = display.screen().root.query_pointer()
        return pointer.root_x, pointer.root_y

    def set_mouse_pos(x, y):
        display.screen().root.warp_pointer(x, y)
        display.sync()


def jiggle(e=12):
    x, y = get_mouse_pos()
    for i in range(1, 4):
        d = int(e / i)
        for dx, dy in [(d, 0), (-d, 0)]:
            set_mouse_pos(x + dx, y + dy)
            time.sleep(.05)
    set_mouse_pos(x, y)


def loop(interval):
    nexttime = time.time() + interval

    while nexttime > time.time():
        time.sleep(1)

    jiggle()
    loop(interval)


def main():
    jiggle()

    parser = argparse.ArgumentParser(description='Jiggle the Mouse')
    parser.add_argument('-n', '--interval', dest='interval', type=int,
            default=180, help='time in seconds between jiggles')

    args = parser.parse_args()

    # If there is no interval, we only
    # jiggle once.
    if args.interval <= 0:
        return

    loop(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

