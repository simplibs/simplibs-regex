from enum import Enum


class AnchorKind(Enum):
    """Which zero-width position assertion an Anchor represents."""

    START = "^"            # start of string, or start of line under MULTILINE
    END = "$"               # end of string, or end of line under MULTILINE
    START_STRING = r"\A"    # start of the whole string, always
    END_STRING = r"\Z"      # end of the whole string, always
    WORD_BOUNDARY = r"\b"
    NON_WORD_BOUNDARY = r"\B"


_DESIGN_NOTES = """
# AnchorKind — Anchor Position Assertion Kind

## Purpose
Defines the specific zero-width position assertion type represented by 
an `Anchor` element (such as line starts, string boundaries, 
or word boundaries).

## Members
- `START`: Matches the start of a line or string.
- `END`: Matches the end of a line or string.
- `START_STRING`: Matches the absolute start of the whole string.
- `END_STRING`: Matches the absolute end of the whole string.
- `WORD_BOUNDARY`: Matches a word boundary.
- `NON_WORD_BOUNDARY`: Matches a non-word boundary.
"""