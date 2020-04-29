import pytest

from tcolorpy import AnsiBGColor, AnsiFGColor, Color, tcolor


class Test_truecolor_color:
    @pytest.mark.parametrize(
        ["string", "color", "expected"],
        [
            ["test", "#ff8822", "\x1b[38;2;255;136;34mtest\x1b[0m"],
            ["test", "ff8822", "\x1b[38;2;255;136;34mtest\x1b[0m"],
            ["test", "red", "\x1b[31mtest\x1b[0m"],
            ["test", Color("red"), "\x1b[31mtest\x1b[0m"],
            ["test", (255, 136, 34), "\x1b[38;2;255;136;34mtest\x1b[0m"],
            ["test", Color("#ff8822"), "\x1b[38;2;255;136;34mtest\x1b[0m"],
            ["test", Color((255, 136, 34)), "\x1b[38;2;255;136;34mtest\x1b[0m"],
            ["test", None, "test"],
        ],
    )
    def test_normal(self, string, color, expected):
        assert tcolor(string, color=color) == expected

    def test_smoke(self):
        string = "test"

        for color in AnsiFGColor:
            assert tcolor(string, color=color) != string

        for color in AnsiBGColor:
            assert tcolor(string, bg_color=color) != string

    @pytest.mark.parametrize(
        ["value", "expected"], [["#fffff", ValueError], ["#GGGGGG", ValueError],],
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            tcolor("test", color=value) == expected


class Test_truecolor_bg_color:
    @pytest.mark.parametrize(
        ["string", "color", "expected"],
        [
            ["test", "#ff8822", "\x1b[48;2;255;136;34mtest\x1b[0m"],
            ["test", "ff8822", "\x1b[48;2;255;136;34mtest\x1b[0m"],
            ["test", "red", "\x1b[41mtest\x1b[0m"],
            ["test", Color("red"), "\x1b[41mtest\x1b[0m"],
            ["test", "light-red", "\x1b[101mtest\x1b[0m"],
            ["test", (255, 136, 34), "\x1b[48;2;255;136;34mtest\x1b[0m"],
            ["test", Color("#ff8822"), "\x1b[48;2;255;136;34mtest\x1b[0m"],
            ["test", Color((255, 136, 34)), "\x1b[48;2;255;136;34mtest\x1b[0m"],
            ["test", None, "test"],
        ],
    )
    def test_normal_bg_color(self, string, color, expected):
        assert tcolor(string, bg_color=color) == expected


class Test_truecolor_fg_bg_color:
    @pytest.mark.parametrize(
        ["string", "color", "bg_color", "expected"],
        [
            ["test", "#111111", "#ffffff", "\x1b[48;2;255;255;255m\x1b[38;2;17;17;17mtest\x1b[0m"],
            ["test", "red", "white", "\x1b[47m\x1b[31mtest\x1b[0m"],
            ["test", None, None, "test"],
        ],
    )
    def test_normal_fg_bg_color(self, string, color, bg_color, expected):
        assert tcolor(string, color=color, bg_color=bg_color) == expected


class Test_truecolor_styles:
    @pytest.mark.parametrize(
        ["string", "styles", "expected"],
        [
            ["test", [], "test"],
            ["test", ["bold"], "\x1b[1mtest\x1b[0m"],
            ["test", ["dim"], "\x1b[2mtest\x1b[0m"],
            ["test", ["italic"], "\x1b[3mtest\x1b[0m"],
            ["test", ["underline"], "\x1b[4mtest\x1b[0m"],
            ["test", ["blink"], "\x1b[5mtest\x1b[0m"],
            ["test", ["invert"], "\x1b[7mtest\x1b[0m"],
            ["test", ["strike"], "\x1b[9mtest\x1b[0m"],
            ["test", ["bold", "dim"], "\x1b[1m\x1b[2mtest\x1b[0m"],
        ],
    )
    def test_normal_bg_color(self, string, styles, expected):
        assert tcolor("test", styles=styles) == expected
