from ...elements.CharacterClass import CharacterClass
from ...elements.CharacterRange import CharacterRange

UPPERCASE_LETTER = CharacterClass(CharacterRange("A", "Z"))
"""Regex expression matching a single uppercase ASCII letter.

Init Params:
    (no parameters)

Pattern:
    Matches one character from `A` to `Z` (`[A-Z]`).

Example:
    UPPERCASE_LETTER
    # Matches: "A", "Z"
    # Does not match: "a", "5"
"""
