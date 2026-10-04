from ...elements.Literal import Literal

NEWLINE = Literal("\n")
"""Regex expression matching a newline character.

Init Params:
    (no parameters)

Pattern:
    Matches the real newline character (`\\n`) exactly once — the character
    itself, not a two-character escape text.

Example:
    NEWLINE
    # Matches: the single newline character
    # Does not match: any other character
"""
