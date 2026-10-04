from ...elements.Literal import Literal

FORM_FEED = Literal("\f")
"""Regex expression matching a form feed character.

Init Params:
    (no parameters)

Pattern:
    Matches the real form feed character (`\\f`) exactly once — the character
    itself, not a two-character escape text.

Example:
    FORM_FEED
    # Matches: the single form feed character
    # Does not match: any other character
"""
