# Outers
from ...elements.Anchor import Anchor, AnchorKind


START = Anchor(AnchorKind.START)
"""Regex expression matching the start of a line.

Init Params:
    (no parameters)

Pattern:
    Matches the position at the start of a line (`^`), respecting multiline mode.

Example:
    START
    # Matches start of any line in multiline text
"""