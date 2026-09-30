# Outers
from ...elements.Anchor import Anchor, AnchorKind


WORD_BOUNDARY = Anchor(AnchorKind.WORD_BOUNDARY)
"""Regex expression matching a word boundary.

Init Params:
    (no parameters)

Pattern:
    Matches a zero-width position where a word character is not followed or preceded by another word-character (`\\b`).

Example:
    WORD_BOUNDARY
    # Matches boundary between a word and a non-word character or edge
"""