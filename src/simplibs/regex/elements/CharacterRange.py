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
    `_usable_in_char_class` atom (`Literal`, `CharacterType`, `CharacterCode`),
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
    def __init__(
        self,
        start: str,
        end: str
    ) -> None:

        # 1. Parameter `start` validation — must be single-character string
        if not isinstance(start, str) or len(start) != 1:
            raise_character_range_invalid_boundary_error("start", start)

        # 2. Parameter `end` validation — must be single-character string
        if not isinstance(end, str) or len(end) != 1:
            raise_character_range_invalid_boundary_error("end", end)

        # 3. Parameter validation — start must not come after end
        if ord(start) > ord(end):
            raise_character_range_start_after_end_error(start, end)

        # 4. Parameter assignment
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
        #    then join with the literal range dash.
        return f"{escape_char_class_char(self.start)}-{escape_char_class_char(self.end)}"

    def __repr__(self) -> str:

        # 1. `to_pattern()` raises for a bare range, so the inherited
        #    repr (which is built from the pattern) cannot be used —
        #    it would crash debuggers and error messages.
        return f"CharacterRange({self.start!r}, {self.end!r})"

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Meaningful only in the sense of "if this were ever queried" —
        #    a range always matches exactly one character, same as any
        #    other CharacterClass item. Included for consistency even
        #    though a bare CharacterRange can never appear inside a
        #    Lookaround directly.
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
