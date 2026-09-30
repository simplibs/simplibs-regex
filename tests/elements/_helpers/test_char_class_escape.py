from simplibs.regex.elements._helpers.char_class_escape import escape_char_class_char

def test_escape_char_class_char():
    """Verify that only character class specials are escaped."""
    assert escape_char_class_char("]") == "\\]"
    assert escape_char_class_char("^") == "\\^"
    assert escape_char_class_char("-") == "\\-"
    assert escape_char_class_char("\\") == "\\\\"
    assert escape_char_class_char("a") == "a"
    assert escape_char_class_char(".") == "."