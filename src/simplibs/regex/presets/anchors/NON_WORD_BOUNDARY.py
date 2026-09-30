# Outers
from ...elements.Anchor import Anchor, AnchorKind


NON_WORD_BOUNDARY = Anchor(AnchorKind.NON_WORD_BOUNDARY)
"""Regex expression matching a non-word boundary.

Init Params:
    (no parameters)

Pattern:
    Matches a zero-width position that is not a word boundary (`\\B`).

Example:
    NON_WORD_BOUNDARY
    # Matches positions inside words (e.g. between 'y' and 't' in 'Python')
"""