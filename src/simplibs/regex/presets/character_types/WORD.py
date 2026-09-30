# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


WORD = CharacterType(CharacterTypeKind.WORD)
"""Regex expression matching a word character.

Init Params:
    (no parameters)

Pattern:
    Matches any letter, digit, or underscore (`\\w`).

Example:
    WORD
    # Matches: "a", "Z", "9", "_"
    # Does not match: " ", "-", "!"
"""