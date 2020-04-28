import pytest
from tcolorpy import Color


class Test_Color:
    @pytest.mark.parametrize(
        ["value", "expected_red", "expected_blue", "expected_green"],
        [
            ["#000000", 0, 0, 0],
            ["#fFfFfF", 255, 255, 255],
            ["#01080f", 1, 8, 15],
            ["000000", 0, 0, 0],
            ["ffffff", 255, 255, 255],
            ["01080f", 1, 8, 15],
            [(0, 0, 0), 0, 0, 0],
            [(1, 8, 15), 1, 8, 15],
        ],
    )
    def test_normal(self, value, expected_red, expected_blue, expected_green):
        color = Color(value)
        assert color.red == expected_red
        assert color.green == expected_blue
        assert color.blue == expected_green

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
            ["red", "invalid color code found"],
        ],
    )
    def test_exception_msg(self, value, expected):
        with pytest.raises(ValueError) as e:
            Color(value)
        assert expected in str(e.value)
