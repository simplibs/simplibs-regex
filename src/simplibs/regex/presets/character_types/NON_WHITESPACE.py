# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


NON_WHITESPACE = CharacterType(CharacterTypeKind.NON_WHITESPACE)
"""Regex expression matching any character that is not whitespace.

Init Params:
    (no parameters)

Pattern:
    Matches any non-whitespace character (`\\S`).

Example:
    NON_WHITESPACE
    # Matches: "a", "5", "!"
    # Does not match: " ", "\\t", "\\n"
"""