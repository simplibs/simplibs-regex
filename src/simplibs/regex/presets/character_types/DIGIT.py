# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


DIGIT = CharacterType(CharacterTypeKind.DIGIT)
"""Regex expression matching a single decimal digit.

Init Params:
    (no parameters)

Pattern:
    Matches any decimal digit from `0` to `9` (`\\d`).

Example:
    DIGIT
    # Matches: "5", "0"
    # Does not match: "a", " "
"""