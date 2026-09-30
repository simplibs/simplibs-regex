from simplibs.regex.presets.character_types import (
    DIGIT,
    NON_DIGIT,
    WORD,
    NON_WORD,
    WHITESPACE,
    NON_WHITESPACE,
)

def test_character_type_presets():
    """Verify that character type presets produce the correct patterns."""
    assert DIGIT.to_pattern() == "\\d"
    assert NON_DIGIT.to_pattern() == "\\D"
    assert WORD.to_pattern() == "\\w"
    assert NON_WORD.to_pattern() == "\\W"
    assert WHITESPACE.to_pattern() == "\\s"
    assert NON_WHITESPACE.to_pattern() == "\\S"