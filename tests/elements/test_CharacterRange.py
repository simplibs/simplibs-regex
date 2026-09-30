import pytest
from simplibs.regex.elements.CharacterRange import CharacterRange


def test_character_range():
    """Verify CharacterRange fragment production and standalone exception."""
    cr = CharacterRange("a", "z")
    assert cr.to_char_class_fragment() == "a-z"
    assert cr.fixed_length() == 1

    with pytest.raises(Exception):
        cr.to_pattern()