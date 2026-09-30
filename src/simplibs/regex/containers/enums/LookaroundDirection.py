from enum import Enum


class LookaroundDirection(Enum):
    """Which side of the current position a Lookaround inspects."""

    AHEAD = "ahead"
    BEHIND = "behind"


_DESIGN_NOTES = """
# LookaroundDirection — Lookaround Assertion Direction

## Purpose
Defines the inspection direction for `Lookaround` assertions 
(whether the inner pattern is evaluated ahead of or behind 
the current match position).

## Members
- `AHEAD`: Inspects forward (right) from the current position.
- `BEHIND`: Inspects backward (left) from the current position, 
enforcing fixed-length constraints.
"""