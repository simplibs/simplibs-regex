from enum import Enum


class CharacterTypeKind(Enum):
    r"""Which built-in character class (\d \D \w \W \s \S)
    a CharacterType represents."""

    DIGIT = r"\d"
    NON_DIGIT = r"\D"
    WORD = r"\w"
    NON_WORD = r"\W"
    WHITESPACE = r"\s"
    NON_WHITESPACE = r"\S"


_DESIGN_NOTES = """
# CharacterTypeKind — Built-In Character Type Kind

## Purpose
Defines the specific built-in Unicode character class represented by 
a `CharacterType` element (such as digits, word characters, or whitespace).

## Members
- `DIGIT`: Matches decimal digits (`\\d`).
- `NON_DIGIT`: Matches non-digit characters (`\\D`).
- `WORD`: Matches word characters (`\\w`).
- `NON_WORD`: Matches non-word characters (`\\W`).
- `WHITESPACE`: Matches whitespace characters (`\\s`).
- `NON_WHITESPACE`: Matches non-whitespace characters (`\\S`).
"""