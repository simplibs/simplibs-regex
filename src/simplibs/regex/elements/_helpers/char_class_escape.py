# `] ^ - \` are special class syntax. `[ & ~ |` are escaped too: `re` reserves
# the doubled forms `[[`, `&&`, `||`, `~~` for future set operations and emits
# a FutureWarning for them (adjacent single-character Literals can form them).
_CHAR_CLASS_SPECIALS = frozenset("]^-\\[&~|")


def escape_char_class_char(char: str) -> str:
    """Escape a single character for use inside a `[...]` character
    class: only the few characters in `_CHAR_CLASS_SPECIALS` — a much
    smaller set than `re.escape`'s general-purpose list, which would
    over-escape harmless characters like `.` or `+` (needlessly
    correct, but misleading to read inside a class where they were
    never special to begin with).
    """
    if char in _CHAR_CLASS_SPECIALS:
        return "\\" + char
    return char


_DESIGN_NOTES = """
# escape_char_class_char — Character Class Escaping

## Purpose
Escapes a single character specifically for use inside a `[...]` character class.

## Why not use general `re.escape`?
`re.escape` escapes a wide range of characters that are harmless inside character 
classes (such as `.` or `+`), which would make the resulting pattern needlessly 
cluttered and harder to read.

## The Special Set (`_CHAR_CLASS_SPECIALS`)
Special class syntax:
- `]` (closing bracket)
- `^` (negation at the start)
- `-` (range separator)
- `\\` (backslash itself)

Escaped for stability (verified against `re.compile`): Python reserves the
doubled sequences `[[`, `&&`, `||`, `~~` (and `--`) inside a class for
future set operations and emits a FutureWarning. Two adjacent
single-character Literals can form them (`Literal("&")`, `Literal("&")`),
so `[ & ~ |` are always escaped; the escaped forms compile cleanly.
"""
