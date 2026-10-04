from ...elements.Literal import Literal

TAB = Literal("\t")
"""Regex expression matching a tab character.

Init Params:
    (no parameters)

Pattern:
    Matches the real tab character (`\\t`) exactly once — the character
    itself, not a two-character escape text.

Example:
    TAB
    # Matches: the single tab character
    # Does not match: any other character
"""
