import re
import warnings
import pytest
from simplibs.regex.elements._helpers import escape_char_class_char


@pytest.mark.parametrize(
    ("char", "fragment"),
    [
        ("a", "a"), (".", "."), ("+", "+"), (" ", " "),
        ("]", "\\]"), ("^", "\\^"), ("-", "\\-"), ("\\", "\\\\"),
        ("[", "\\["), ("&", "\\&"), ("~", "\\~"), ("|", "\\|"),
        ("\t", "\\t"), ("\n", "\\n"), ("\r", "\\r"), ("\f", "\\f"), ("\v", "\\v"), ("\a", "\\a"),
        ("\x08", "\\x08"), ("\x00", "\\x00"), ("\x7f", "\\x7f"),
    ],
)
def test_escape_char_class_char(char, fragment):
    assert escape_char_class_char(char) == fragment


def test_every_escaped_character_is_matched_inside_a_class_without_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        for code in list(range(0x300)) + [0x2028, 0x1F600]:
            char = chr(code)
            compiled = re.compile("[" + escape_char_class_char(char) * 2 + "]")   # doubled: &&, ||, ~~ must not warn
            assert compiled.fullmatch(char) is not None, hex(code)
