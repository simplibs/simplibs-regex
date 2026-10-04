from ...elements.CharacterClass import CharacterClass
from ...elements.CharacterRange import CharacterRange

LOWERCASE_LETTER = CharacterClass(CharacterRange("a", "z"))
"""Regex expression matching a single lowercase ASCII letter.

Init Params:
    (no parameters)

Pattern:
    Matches one character from `a` to `z` (`[a-z]`).

Example:
    LOWERCASE_LETTER
    # Matches: "a", "z"
    # Does not match: "A", "5", "é"
"""
