# Outers
from ..base_class import Regex
# Inners
from ._helpers import escape_char_class_char
from ._validations import (
    raise_character_range_invalid_boundary_error,
    raise_character_range_start_after_end_error,
    raise_character_range_no_standalone_pattern_error,
)


class CharacterRange(Regex):
    """A contiguous range of characters, e.g. `a-z`.

    Only ever legal as a standalone item inside a `CharacterClass` — a
    range has no standalone meaning outside `[...]`, unlike every other
    `_usable_in_char_class` atom (`Literal`, `CharacterType`, `CharCode`),
    which all also make sense on their own. `to_pattern()` therefore
    deliberately raises rather than silently producing something
    meaningless.

    Example:
        CharacterClass(CharacterRange("a", "z"))   # -> "[a-z]"
    """

    __slots__ = ("start", "end")

    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, start: str, end: str) -> None:

        # 1. Parameter validation — both must be single characters[cite: 26]
        for name, value in (("start", start), ("end", end)):
            if not (isinstance(value, str) and len(value) == 1):
                raise_character_range_invalid_boundary_error(name, value)

        # 2. Parameter validation — start must not come after end[cite: 26]
        if ord(start) > ord(end):
            raise_character_range_start_after_end_error(start, end)

        # 3. Parameter assignment
        self.start = start
        self.end = end

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:
        raise_character_range_no_standalone_pattern_error()

    def to_char_class_fragment(self) -> str:

        # 1. Escape start/end individually (only relevant for `]`/`^`
        #    landing at a range boundary, e.g. CharacterRange('[', ']')),
        #    then join with the literal range dash[cite: 26].
        return f"{escape_char_class_char(self.start)}-{escape_char_class_char(self.end)}"

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Meaningful only in the sense of "if this were ever queried" —
        #    a range always matches exactly one character, same as any
        #    other CharacterClass item[cite: 26]. Included for consistency even
        #    though a bare CharacterRange can never appear inside a
        #    Lookaround directly[cite: 26].
        return 1

_DESIGN_NOTES = """
# CharacterRange — Range-Only CharacterClass Item

## Why `to_pattern` raises instead of returning something
Every other node in the hierarchy can be rendered standalone, even if
that standalone rendering is rarely useful on its own. `CharacterRange`
genuinely has no meaning outside `[...]` — `a-z` at the top level of a
pattern would just match the three literal characters `a`, `-`, `z` in
sequence, which is not what constructing a `CharacterRange` expresses.
Raising here (rather than silently producing a misleading fragment)
turns an easy mistake — accidentally using a `CharacterRange` outside a
`CharacterClass` — into an immediate, clear error instead of a subtly
wrong compiled pattern.

## Escaping the boundary characters individually
`CharacterRange('[', ']')` — an unusual but legal range spanning the
bracket characters — needs each boundary escaped independently before
joining with `-`; reusing `escape_char_class_char` (the same helper
`Literal.to_char_class_fragment` uses) keeps that one escaping rule
defined in exactly one place, per the same reasoning `AllOf`/`AnyOf`
share `build_child_exception` instead of each reimplementing it.
"""
