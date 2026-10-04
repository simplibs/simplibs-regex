from .Alternation import Alternation
from .Conditional import Conditional
from .Group import Group
from .Lookaround import Lookaround
from .Repeat import Repeat
from .Sequence import Sequence
from .enums import LookaroundDirection, RepeatMode


_DESIGN_NOTES = """
# Regex Containers Sub-Package

## Purpose
The `containers` package provides higher-order AST node containers that combine, quantify, 
group, or conditionally structure multiple regex nodes into complex patterns, along with their governing enums.

## Internal Components Registry

| Component             | Type             | Description                                                                     |
| :-------------------- | :--------------- | :------------------------------------------------------------------------------ |
| `Alternation`         | Container Class  | Matches any of multiple alternative sub-patterns (`a|b`).                       |
| `Conditional`         | Container Class  | Conditional matching based on group existence or check condition.               |
| `Group`               | Container Class  | Grouping, capturing, non-capturing, or named sub-patterns (`(...)`).            |
| `Lookaround`          | Container Class  | Zero-width positive/negative lookahead or lookbehind assertions.                |
| `LookaroundDirection` | Enum             | Specifies whether a lookaround assertion inspects ahead or behind.     |
| `Repeat`              | Container Class  | Quantifies sub-patterns with specified min, max, and greediness modes.          |
| `RepeatMode`          | Enum             | Specifies the backtracking behavior of a quantifier (greedy, lazy, possessive). |
| `Sequence`            | Container Class  | Matches a sequential chain of sub-patterns in order (`abc`).                    |
"""


