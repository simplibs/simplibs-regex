# Outers
from ...elements.Anchor import Anchor, AnchorKind

END_STRING = Anchor(AnchorKind.END_STRING)
"""Regex expression matching the absolute end of the string.

Init Params:
    (no parameters)

Pattern:
    Matches the absolute end of the entire text (`\\Z`), unaffected by multiline mode.

Example:
    END_STRING
    # Matches only at the very end of the string
"""