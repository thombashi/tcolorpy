#!/usr/bin/env python3

import sys

from tcolorpy import AnsiBGColor, AnsiFGColor, tcolor


def main() -> int:
    template = "{:26} {:26} {:26}"

    print(
        template.format(
            tcolor("color", color="white"),
            tcolor("bg_color", color="white"),
            tcolor("invert", color="white"),
        )
    )
    print("━" * 50)
    for fg_color, bg_color in zip(AnsiFGColor, AnsiBGColor):
        print(
            template.format(
                tcolor(fg_color.name, color=fg_color),
                tcolor(bg_color.name, bg_color=bg_color),
                tcolor(fg_color.name, color=fg_color, styles=["invert"]),
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
