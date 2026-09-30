# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


NON_WORD = CharacterType(CharacterTypeKind.NON_WORD)
"""Regex expression matching any character that is not a word character.

Init Params:
    (no parameters)

Pattern:
    Matches any non-word character (`\\W`).

Example:
    NON_WORD
    # Matches: " ", "-", "!"
    # Does not match: "a", "5", "_"
"""