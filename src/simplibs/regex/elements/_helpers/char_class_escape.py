_CHAR_CLASS_SPECIALS = frozenset("]^-\\")


def escape_char_class_char(char: str) -> str:
    """Escape a single character for use inside a `[...]` character
    class, per Point 4: only `] ^ - \\` are special in this context — a
    much smaller set than `re.escape`'s general-purpose list, which
    would over-escape harmless characters like `.` or `+` (needlessly
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

## The Minimal Special Set (`_CHAR_CLASS_SPECIALS`)
Inside `[...]`, only four characters have special meaning and require escaping:
- `]` (closing bracket)
- `^` (negation at the start)
- `-` (range separator)
- `\\` (backslash itself)
"""