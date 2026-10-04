# Outers
from ...elements.CharacterType import CharacterType, CharacterTypeKind


DIGIT = CharacterType(CharacterTypeKind.DIGIT)
"""Regex expression matching a single decimal digit.

Init Params:
    (no parameters)

Pattern:
    Matches any Unicode decimal digit (`\\d`): `0`-`9` and digits of other
    scripts. Compile with the ASCII flag to restrict it to `0`-`9`.

Example:
    DIGIT
    # Matches: "5", "0"
    # Does not match: "a", " "
"""
