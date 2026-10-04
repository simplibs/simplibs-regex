# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


WORD = CharacterType(CharacterTypeKind.WORD)
"""Regex expression matching a word character.

Init Params:
    (no parameters)

Pattern:
    Matches any Unicode letter, digit, or underscore (`\\w`). Under the ASCII
    flag only `a-z`, `A-Z`, `0-9` and `_`.

Example:
    WORD
    # Matches: "a", "Z", "9", "_"
    # Does not match: " ", "-", "!"
"""
