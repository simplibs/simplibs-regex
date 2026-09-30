# Outers
from ...elements.Anchor import Anchor, AnchorKind


END = Anchor(AnchorKind.END)
"""Regex expression matching the end of a line.

Init Params:
    (no parameters)

Pattern:
    Matches the position at the end of a line (`$`), respecting multiline mode.

Example:
    END
    # Matches end of any line in multiline text
"""