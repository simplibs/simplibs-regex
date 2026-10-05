from ...elements.Literal import Literal

BACKSLASH = Literal("\\")
"""Regex expression matching a literal backslash character.

Init Params:
    (no parameters)

Pattern:
    Matches the real backslash character (`\\`) exactly once — the character
    itself, not a two-character escape text.

Example:
    BACKSLASH
    # Matches: the single backslash character
    # Does not match: any other character
"""
