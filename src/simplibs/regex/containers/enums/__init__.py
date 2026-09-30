from .LookaroundDirection import LookaroundDirection
from .RepeatMode import RepeatMode


_DESIGN_NOTES = """
# Containers Enums Sub-Package

## Purpose
The `enums` package provides internal and structural enumeration types used 
by regex container nodes to govern behavior, such as repetition backtracking 
modes and lookaround inspection directions.

## Internal Components Registry

| Component             | Type   | Description                                                                     |
| :-------------------- | :----- | :------------------------------------------------------------------------------ |
| `LookaroundDirection` | Enum   | Specifies whether a lookaround assertion inspects ahead or behind[cite: 9].     |
| `RepeatMode`          | Enum   | Specifies the backtracking behavior of a quantifier (greedy, lazy, possessive)[cite: 10]. |
"""
