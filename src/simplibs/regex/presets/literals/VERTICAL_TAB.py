from ...elements.Literal import Literal

VERTICAL_TAB = Literal("\v")
"""Regex expression matching a vertical tab character.

Init Params:
    (no parameters)

Pattern:
    Matches the real vertical tab character (`\\v`) exactly once — the character
    itself, not a two-character escape text.

Example:
    VERTICAL_TAB
    # Matches: the single vertical tab character
    # Does not match: any other character
"""
