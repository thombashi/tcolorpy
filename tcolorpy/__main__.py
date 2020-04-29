#!/usr/bin/env python3

import argparse
import sys

from ._const import AnsiBGColor, AnsiFGColor, AnsiStyle
from ._truecolor import tcolor


def parse_option() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("string", help="string to apply styles.")
    parser.add_argument(
        "-c",
        "--color",
        help="specify a color code (#XXXXXX) or a name. valid names are: {}".format(
            ", ".join([style.name.lower() for style in list(AnsiFGColor)])
        ),
    )
    parser.add_argument(
        "-b",
        "--bg-color",
        help="specify a background color code (#XXXXXX) or a name. valid names are: {}".format(
            ", ".join([style.name.lower() for style in list(AnsiBGColor)])
        ),
    )
    parser.add_argument(
        "-s",
        "--styles",
        help="specify a comma separated styles. valid values are: {}".format(
            ", ".join([style.name.lower() for style in list(AnsiStyle)])
        ),
    )

    return parser.parse_args()


def main() -> int:
    ns = parse_option()

    styles = []
    if ns.styles:
        styles = [style for style in ns.styles.split(",")]

    try:
        print(tcolor(ns.string, color=ns.color, bg_color=ns.bg_color, styles=styles))
    except ValueError as e:
        print("{}: {}".format(e.__class__.__name__, e), file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
