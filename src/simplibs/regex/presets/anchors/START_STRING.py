# Outers
from ...elements.Anchor import Anchor, AnchorKind


START_STRING = Anchor(AnchorKind.START_STRING)
"""Regex expression matching the absolute start of the string.

Init Params:
    (no parameters)

Pattern:
    Matches the absolute start of the entire text (`\\A`), unaffected by multiline mode.

Example:
    START_STRING
    # Matches only at the very beginning of the string
"""