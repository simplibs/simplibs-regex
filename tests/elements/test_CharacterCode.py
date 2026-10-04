import re

import pytest
from simplibs.regex.elements.CharacterCode import CharacterCode, CharacterCodeKind


def test_char_code() -> None:
    """Verify CharacterCode pattern production for various kinds."""
    assert CharacterCode(CharacterCodeKind.HEX, 0x41).to_pattern() == "\\x41"
    assert CharacterCode(CharacterCodeKind.UNICODE_SHORT, 0xFFFF).to_pattern() == "\\uffff"
    assert CharacterCode(CharacterCodeKind.UNICODE_LONG, 0x10FFFF).to_pattern() == "\\U0010ffff"
    assert CharacterCode(CharacterCodeKind.NAMED, "BULLET").to_pattern() == "\\N{BULLET}"
    assert CharacterCode(CharacterCodeKind.OCTAL, 0o77).to_pattern() == "\\077"
    assert CharacterCode(CharacterCodeKind.HEX, 0x41).fixed_length() == 1


def test_char_code_octal_upper_bound() -> None:
    """Octal 0o377 is the last legal value; 0o400 must be rejected at construction."""
    node = CharacterCode(CharacterCodeKind.OCTAL, 0o377)
    assert node.to_pattern() == "\\377"
    re.compile(node.to_pattern())  # really is valid for `re`

    with pytest.raises(ValueError):
        CharacterCode(CharacterCodeKind.OCTAL, 0o400)

    with pytest.raises(re.error):  # confirms the boundary comes from `re` itself
        re.compile("\\400")


def test_char_code_hex_out_of_range() -> None:
    """A HEX value above 0xFF is rejected at construction."""
    with pytest.raises(ValueError):
        CharacterCode(CharacterCodeKind.HEX, 0x100)


@pytest.mark.parametrize("name", ["BULLET", "bullet", "LINE FEED"])
def test_named_accepts_known_names(name):
   assert CharacterCode(CharacterCodeKind.NAMED, name).to_pattern() == f"\\N{{{name}}}"


@pytest.mark.parametrize("name", ["NOPE", "KATAKANA LETTER AINU P"])
def test_named_rejects_unknown_names(name):
   with pytest.raises(ValueError):
       CharacterCode(CharacterCodeKind.NAMED, name)
