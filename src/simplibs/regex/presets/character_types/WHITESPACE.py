# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


WHITESPACE = CharacterType(CharacterTypeKind.WHITESPACE)
"""Regex expression matching a whitespace character.

Init Params:
    (no parameters)

Pattern:
    Matches any whitespace character like space, tab, or newline (`\\s`).

Example:
    WHITESPACE
    # Matches: " ", "\\t", "\\n"
    # Does not match: "a", "5"
"""