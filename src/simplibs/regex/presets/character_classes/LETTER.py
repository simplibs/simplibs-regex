from ...elements.CharacterClass import CharacterClass
from ...elements.CharacterRange import CharacterRange

LETTER = CharacterClass(CharacterRange("a", "z"), CharacterRange("A", "Z"))
"""Regex expression matching a single ASCII letter.

Init Params:
    (no parameters)

Pattern:
    Matches one lowercase or uppercase ASCII letter (`[a-zA-Z]`).

Example:
    LETTER
    # Matches: "a", "Z"
    # Does not match: "5", "_", "é"
"""
