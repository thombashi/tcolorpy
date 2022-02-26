#!/usr/bin/env python3

import sys

from tcolorpy import Color, tcolor


def print_truecolor(c: Color) -> None:
    end = "   "
    print(tcolor(c.color_code, bg_color=c), end=end)
    print(tcolor(c.color_code, color=c), end=end)
    print(tcolor(c.color_code, color=c, styles=["bold"]), end=end)
    print(tcolor(c.color_code, color=c, styles=["dim"]), end=end)
    print(tcolor(c.color_code, color=c, styles=["italic"]), end=end)
    print(tcolor(c.color_code, color=c, styles=["underline"]), end=end)
    print(tcolor(c.color_code, color=c, styles=["invert"]), end=end)
    print(tcolor(c.color_code, color=c, styles=["strike"]), end=end)
    print()


def main() -> int:
    step = 32

    print(
        "bg_color  {color}     {bold}      {dim}       {italic}    {underline} {invert}    {strike}".format(  # noqa
            color="color",
            bold=tcolor("bold", styles=["bold"]),
            dim=tcolor("dim", styles=["dim"]),
            italic=tcolor("italic", styles=["italic"]),
            underline=tcolor("underline", styles=["underline"]),
            invert=tcolor("invert", styles=["invert"]),
            strike=tcolor("strike", styles=["strike"]),
        )
    )

    for i in range(0, 255, step):
        print_truecolor(Color((255, i, 0)))

    for i in range(0, 255, step):
        print_truecolor(Color((255 - i, 255, 0)))

    for i in range(0, 255, step):
        print_truecolor(Color((0, 255, i)))

    for i in range(0, 255, step):
        print_truecolor(Color((0, 255 - i, 255)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
