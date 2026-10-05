from .escape_control_character import escape_control_character

# `] ^ - \\` are special class syntax. `[ & ~ |` are escaped too: `re` reserves
# the doubled forms `[[`, `&&`, `||`, `~~` for future set operations and emits
# a FutureWarning for them (adjacent single-character Literals can form them).
_CHAR_CLASS_SPECIALS = frozenset("]^-\\[&~|")


def escape_char_class_char(char: str) -> str:
    """Escape a single character for use inside a `[...]` character
    class: control characters become readable escapes (`\\t`, `\\n`, ...), the
    few class specials in `_CHAR_CLASS_SPECIALS` get a backslash — a much
    smaller set than `re.escape`'s general-purpose list, which would
    over-escape harmless characters like `.` or `+` (needlessly
    correct, but misleading to read inside a class where they were
    never special to begin with).
    """
    control = escape_control_character(char)
    if control is not None:
        return control

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

## Control characters
Written as readable escapes (`\\t`, `\\n`, `\\xhh`, ...) by the shared
`escape_control_character`, so a class such as `[^,\\r\\n]` is visible in the
pattern string instead of containing raw, invisible characters.
"""
