from enum import Enum


class RepeatMode(Enum):
    """Backtracking behavior of a Repeat quantifier."""

    GREEDY = ""       # match as much as possible, backtrack if needed
    LAZY = "?"         # match as little as possible, expand if needed
    POSSESSIVE = "+"   # match as much as possible, NEVER backtrack (3.11+)


_DESIGN_NOTES = """
# RepeatMode — Quantifier Backtracking Mode

## Purpose
Defines the backtracking behavior modifier for `Repeat` quantifiers 
(greedy, lazy, or possessive).

## Members
- `GREEDY`: Matches as much as possible and backtracks if needed (default).
- `LAZY`: Matches as little as possible and expands if needed.
- `POSSESSIVE`: Matches as much as possible and never backtracks.
"""