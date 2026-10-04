from ...elements.CharacterClass import CharacterClass
from ...elements.CharacterRange import CharacterRange

HEX_DIGIT = CharacterClass(CharacterRange("0", "9"), CharacterRange("a", "f"), CharacterRange("A", "F"))
"""Regex expression matching a single hexadecimal digit.

Init Params:
    (no parameters)

Pattern:
    Matches one hexadecimal digit, case-insensitive by range (`[0-9a-fA-F]`).

Example:
    HEX_DIGIT
    # Matches: "0", "9", "a", "F"
    # Does not match: "g", "-"
"""
