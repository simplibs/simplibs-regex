from ...elements.CharacterClass import CharacterClass
from ...elements.CharacterRange import CharacterRange

ALPHANUMERIC = CharacterClass(CharacterRange("a", "z"), CharacterRange("A", "Z"), CharacterRange("0", "9"))
"""Regex expression matching a single ASCII letter or digit.

Init Params:
    (no parameters)

Pattern:
    Matches one ASCII letter or digit (`[a-zA-Z0-9]`); no underscore, no non-ASCII digits.

Example:
    ALPHANUMERIC
    # Matches: "a", "Z", "5"
    # Does not match: "_", "-", "é"
"""
