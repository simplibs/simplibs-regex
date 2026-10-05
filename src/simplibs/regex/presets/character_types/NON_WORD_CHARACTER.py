# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


NON_WORD_CHARACTER = CharacterType(CharacterTypeKind.NON_WORD_CHARACTER)
"""Regex expression matching any character that is not a word character.

Init Params:
    (no parameters)

Pattern:
    Matches any non-word character (`\\W`).

Example:
    NON_WORD_CHARACTER
    # Matches: " ", "-", "!"
    # Does not match: "a", "5", "_"
"""