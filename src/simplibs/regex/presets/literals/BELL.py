from ...elements.Literal import Literal

BELL = Literal("\a")
"""Regex expression matching a bell (alert) character.

Init Params:
    (no parameters)

Pattern:
    Matches the real bell character (`\\a`) exactly once — the character
    itself, not a two-character escape text.

Example:
    BELL
    # Matches: the single bell character
    # Does not match: any other character
"""
