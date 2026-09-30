# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


NON_DIGIT = CharacterType(CharacterTypeKind.NON_DIGIT)
"""Regex expression matching any character that is not a decimal digit.

Init Params:
    (no parameters)

Pattern:
    Matches any character except decimal digits (`\\D`).

Example:
    NON_DIGIT
    # Matches: "a", " ", "-"
    # Does not match: "5"
"""