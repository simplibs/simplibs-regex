from simplibs.regex.elements.CharCode import CharCode, CharCodeKind

def test_char_code():
    """Verify CharCode pattern production for various kinds."""
    assert CharCode(CharCodeKind.HEX, 0x41).to_pattern() == "\\x41"
    assert CharCode(CharCodeKind.UNICODE_SHORT, 0xFFFF).to_pattern() == "\\uffff"
    assert CharCode(CharCodeKind.UNICODE_LONG, 0x10FFFF).to_pattern() == "\\U0010ffff"
    assert CharCode(CharCodeKind.NAMED, "BULLET").to_pattern() == "\\N{BULLET}"
    assert CharCode(CharCodeKind.OCTAL, 0o77).to_pattern() == "\\077"
    assert CharCode(CharCodeKind.HEX, 0x41).fixed_length() == 1