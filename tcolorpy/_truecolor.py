import re
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Type, Union, cast  # noqa

from ._const import CSI, RESET, AnsiBackColor, AnsiFGColor, AnsiStyle


RGBTuple = Tuple[int, int, int]

_regexp_color_code = re.compile(
    "^#?(?P<red>[0-9a-f]{2})(?P<green>[0-9a-f]{2})(?P<blue>[0-9a-f]{2})$", re.IGNORECASE
)
_regexp_normalize = re.compile(r"[\s_-]")
name_to_rgb = {
    "BLACK": (0, 0, 0),
    "RED": (205, 49, 49),
    "GREEN": (13, 188, 121),
    "YELLOW": (229, 229, 16),
    "BLUE": (36, 114, 200),
    "MAGENTA": (188, 63, 188),
    "CYAN": (17, 168, 205),
    "WHITE": (229, 229, 229),
    "LIGHTBLACK": (102, 102, 102),
    "LIGHTRED": (241, 76, 76),
    "LIGHTGREEN": (35, 209, 139),
    "LIGHTYELLOW": (245, 245, 67),
    "LIGHTBLUE": (59, 142, 234),
    "LIGHTMAGENTA": (214, 112, 214),
    "LIGHTCYAN": (41, 184, 219),
    "LIGHTWHITE": (255, 255, 255),
}


def _normalize_name(name: str) -> str:
    return _regexp_normalize.sub("", name).upper()


class Color:
    def __init__(self, color: Union[str, RGBTuple]) -> None:
        self.__is_color_code_src = False

        if isinstance(color, str):
            color = _normalize_name(color)
            try:
                self.__from_color_name(color)
            except KeyError:
                self.__from_color_code(color)

            return

        self.red, self.green, self.blue = color
        self.__validate_color_value(self.red)
        self.__validate_color_value(self.green)
        self.__validate_color_value(self.blue)

    def __from_color_code(self, color_code: str) -> None:
        match = _regexp_color_code.search(color_code)
        if match is None:
            raise ValueError("invalid color code found: {}".format(color_code))

        self.__is_color_code_src = True
        red, green, blue = match.group(1, 2, 3)
        self.red = int(red, 16)
        self.green = int(green, 16)
        self.blue = int(blue, 16)

    def __from_color_name(self, name: str) -> None:
        self.red, self.green, self.blue = name_to_rgb[name]

    def __validate_color_value(self, n: int) -> None:
        if not (0 <= n <= 255):
            raise ValueError("value must be within 0-255")

    @property
    def is_color_code_src(self) -> bool:
        return self.__is_color_code_src

    @property
    def color_code(self) -> str:
        return "#{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue)

    def calc_complementary(self):
        rgb = (self.red, self.green, self.blue)
        n = max(rgb) + min(rgb)
        return Color((n - self.red, n - self.green, n - self.blue))


def _normalize_enum(value, enum_class: Type[Enum]):
    if isinstance(value, enum_class):
        return value

    try:
        return enum_class[_normalize_name(value)]
    except AttributeError:
        raise TypeError("value must be a {} or a str: actual={}".format(enum_class, type(value)))
    except KeyError:
        raise ValueError(
            "invalid valid found: expected={}, actual={}".format(
                "/".join([item.name for item in enum_class]), value
            )
        )


def _ansi_escape(value: str) -> str:
    return "{}{}m".format(CSI, value)


def _to_ansi_style(style: Union[str, AnsiStyle]) -> str:
    return _ansi_escape("{}".format(_normalize_enum(style, AnsiStyle).value))


def _to_ansi_fg_truecolor(color: Color) -> str:
    return _ansi_escape("38;2;{};{};{}".format(color.red, color.green, color.blue))


def _to_ansi_bg_truecolor(color: Color) -> str:
    return _ansi_escape("48;2;{};{};{}".format(color.red, color.green, color.blue))


def _to_ansi_fg_color(color: AnsiFGColor) -> str:
    return _ansi_escape("{}".format(color.value))


def _to_ansi_bg_color(color: AnsiBackColor) -> str:
    return _ansi_escape("{}".format(color.value))


def _make_ansi_fg_truecolor(color: Union[Color, str, RGBTuple, AnsiFGColor, None]) -> str:
    if isinstance(color, AnsiFGColor):
        return _to_ansi_fg_color(color)

    if isinstance(color, str):
        try:
            return _to_ansi_fg_color(_normalize_enum(color, AnsiFGColor))
        except ValueError:
            c = Color(color)

    elif isinstance(color, (tuple, list)):
        c = Color(color)
    else:
        c = color  # type: ignore

    return _to_ansi_fg_truecolor(c) if c else ""


def _make_ansi_bg_truecolor(color: Union[Color, str, RGBTuple, AnsiBackColor, None]) -> str:
    if isinstance(color, AnsiBackColor):
        return _to_ansi_bg_color(color)

    if isinstance(color, str):
        try:
            return _to_ansi_bg_color(_normalize_enum(color, AnsiBackColor))
        except ValueError:
            c = Color(color)
    elif isinstance(color, (tuple, list)):
        c = Color(color)
    else:
        c = color  # type: ignore

    return _to_ansi_bg_truecolor(c) if c else ""


def tcolor(
    string: str,
    color: Union[Color, str, RGBTuple, AnsiFGColor, None] = None,
    bg_color: Union[Color, str, RGBTuple, AnsiBackColor, None] = None,
    styles: Optional[Sequence[Union[str, AnsiStyle]]] = None,
) -> str:
    ansi_fg_color = _make_ansi_fg_truecolor(color)
    ansi_bg_color = _make_ansi_bg_truecolor(bg_color)

    ansi_styles = []  # type: List[str]
    if styles:
        ansi_styles = [_to_ansi_style(style) for style in styles]

    reset = RESET
    if not ansi_fg_color and not ansi_bg_color and not ansi_styles:
        reset = ""

    return "".join(ansi_styles + [ansi_bg_color, ansi_fg_color, string, reset])
