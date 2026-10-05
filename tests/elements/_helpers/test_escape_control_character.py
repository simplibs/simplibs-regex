import re
import pytest
from simplibs.regex.elements._helpers import escape_control_character


@pytest.mark.parametrize(
    ("char", "escape"),
    [("\t", "\\t"), ("\n", "\\n"), ("\r", "\\r"), ("\f", "\\f"), ("\v", "\\v"), ("\a", "\\a"),
     ("\x00", "\\x00"), ("\x08", "\\x08"), ("\x1b", "\\x1b"), ("\x1f", "\\x1f"), ("\x7f", "\\x7f")],
)
def test_control_characters_become_readable_escapes(char, escape):
    assert escape_control_character(char) == escape
    assert re.fullmatch(escape, char) is not None


def test_backspace_is_not_written_as_b():
    """Outside a class `\\b` is a word boundary, so U+0008 must be `\\x08`."""
    assert escape_control_character("\x08") == "\\x08"


@pytest.mark.parametrize("char", ["a", " ", ".", "\\", "é", "~", "\x80", "\u2028"])
def test_other_characters_are_left_to_the_caller(char):
    assert escape_control_character(char) is None


def test_every_control_character_round_trips_through_re():
    for code in list(range(0x20)) + [0x7F]:
        char = chr(code)
        assert re.fullmatch(escape_control_character(char), char) is not None, hex(code)
