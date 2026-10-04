from ...elements.Literal import Literal

CARRIAGE_RETURN = Literal("\r")
"""Regex expression matching a carriage return character.

Init Params:
    (no parameters)

Pattern:
    Matches the real carriage return character (`\\r`) exactly once — the character
    itself, not a two-character escape text.

Example:
    CARRIAGE_RETURN
    # Matches: the single carriage return character
    # Does not match: any other character
"""
