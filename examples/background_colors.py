#!/usr/bin/env python3

import sys

from tcolorpy import Color, tcolor


def main() -> int:
    string = " "
    step = 8
    line = ""

    for i in range(0, 255, step):
        line += tcolor(string, bg_color=Color((255, i, 0)))

    for i in range(0, 255, step):
        line += tcolor(string, bg_color=Color((255 - i, 255, 0)))

    for i in range(0, 255, step):
        line += tcolor(string, bg_color=Color((0, 255, i)))

    for i in range(0, 255, step):
        line += tcolor(string, bg_color=Color((0, 255 - i, 255)))

    for r in range(16):
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
