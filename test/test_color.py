import pytest

from tcolorpy import Color
from tcolorpy._truecolor import name_to_rgb


class Test_Color_constructor:
    @pytest.mark.parametrize(
        ["value", "expected_red", "expected_blue", "expected_green", "is_color_code_src"],
        [
            ["#000000", 0, 0, 0, True],
            ["#fFfFfF", 255, 255, 255, True],
            ["#01080f", 1, 8, 15, True],
            ["000000", 0, 0, 0, True],
            ["ffffff", 255, 255, 255, True],
            ["01080f", 1, 8, 15, True],
            ["light-red", *name_to_rgb["LIGHTRED"], False],
            ["light_red", *name_to_rgb["LIGHTRED"], False],
            ["LightRed", *name_to_rgb["LIGHTRED"], False],
            [(0, 0, 0), 0, 0, 0, False],
            [(1, 8, 15), 1, 8, 15, False],
        ]
        + [[value, *rgb, False] for value, rgb in name_to_rgb.items()],
    )
    def test_normal(self, value, expected_red, expected_blue, expected_green, is_color_code_src):
        color = Color(value)
        assert color.red == expected_red
        assert color.green == expected_blue
        assert color.blue == expected_green
        assert color.is_color_code_src == is_color_code_src

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [None, TypeError],
            [(256, 0, 0), ValueError],
            [(0, 256, 0), ValueError],
            [(0, 0, 256), ValueError],
            [(-1, 0, 0), ValueError],
            [(0, -1, 0), ValueError],
            [(0, 0, -1), ValueError],
        ],
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            Color(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["", "invalid color code found"],
            ["#GGGGGG", "invalid color code found"],
            ["#afafa", "invalid color code found"],
            ["redg", "invalid color code found"],
        ],
    )
    def test_exception_msg(self, value, expected):
        with pytest.raises(ValueError) as e:
            Color(value)
        assert expected in str(e.value)


class Test_Color_eq:
    def test_normal(self):
        black_rgb = Color("#000000")
        red_rgb = Color("#ff0000")
        black_name = Color("black")

        assert black_rgb == black_rgb
        assert black_name == black_name
        assert black_rgb != red_rgb
        assert black_rgb != black_name
