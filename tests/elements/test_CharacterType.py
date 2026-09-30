from simplibs.regex.elements.CharacterType import CharacterType, CharacterTypeKind

def test_character_type():
    """Verify CharacterType pattern production and fixed length."""
    assert CharacterType(CharacterTypeKind.DIGIT).to_pattern() == "\\d"
    assert CharacterType(CharacterTypeKind.NON_DIGIT).to_pattern() == "\\D"
    assert CharacterType(CharacterTypeKind.WORD).to_pattern() == "\\w"
    assert CharacterType(CharacterTypeKind.NON_WORD).to_pattern() == "\\W"
    assert CharacterType(CharacterTypeKind.WHITESPACE).to_pattern() == "\\s"
    assert CharacterType(CharacterTypeKind.NON_WHITESPACE).to_pattern() == "\\S"
    assert CharacterType(CharacterTypeKind.DIGIT).fixed_length() == 1