# Outers
from ..base_class import Regex
# Inners
from ._validations import (
    raise_group_reference_numeric_out_of_range_error,
    raise_group_reference_invalid_identifier_error,
    raise_group_reference_invalid_type_error,
)


class GroupReference(Regex):
    """Backreference to a previously captured group, by number or name.

    Pattern:
        \\1              id_or_name is an int
        (?P=name)        id_or_name is a str

    Example:
        GroupReference(1)          # -> "\\1"
        GroupReference("year")     # -> "(?P=year)"
    """

    __slots__ = ("id_or_name",)

    # Deliberately left at the base class default (False): `\1` inside a
    # CharacterClass is an OCTAL escape, not a backreference — the two
    # contexts mean genuinely different things, so a GroupReference is
    # never a legal CharacterClass item (unlike CharacterType/CharCode,
    # where the meaning is identical either side of `[...]`)[cite: 29].

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, id_or_name: int | str) -> None:

        # 1. Parameter validation
        if isinstance(id_or_name, int):
            if id_or_name < 1:
                raise_group_reference_numeric_out_of_range_error(id_or_name)
        elif isinstance(id_or_name, str):
            if not id_or_name.isidentifier():
                raise_group_reference_invalid_identifier_error(id_or_name)
        else:
            raise_group_reference_invalid_type_error(id_or_name)

        # 2. Parameter assignment
        self.id_or_name = id_or_name

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Numeric id -> \1 syntax; name -> (?P=name) syntax[cite: 29].
        if isinstance(self.id_or_name, int):
            return f"\\{self.id_or_name}"
        return f"(?P={self.id_or_name})"

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Genuinely unknowable in general — a backreference's match
        #    width depends entirely on whatever text the referenced
        #    group actually captured at runtime, which this static tree
        #    has no way to know (the referenced Group node isn't even
        #    reachable from here — GroupReference stores only an id/name,
        #    not a pointer back to the Group it refers to)[cite: 29].
        return None


_DESIGN_NOTES = """
# GroupReference — Numeric and Named Backreferences

## Why it is never usable inside a CharacterClass
This is the sharpest example of Point 4 in the whole library: `\\1`
OUTSIDE a character class is a backreference, but `\\1` INSIDE `[...]`
is an octal escape (character code 1) — genuinely different meanings for
the identical text. Leaving `_usable_in_char_class` at its base-class
`False` default (rather than needing a special-case check anywhere)
is exactly what that flag exists to prevent: silently reusing a
`GroupReference` where its rendered text would mean something entirely
different.

## Why `fixed_length` is unconditionally None
Unlike `Anchor`/`CharacterType` (always genuinely 0 or 1), a
backreference's width is a real runtime unknown from a static tree's
point of view — it depends on what the referenced group actually
matched. Returning `None` is the only honest answer; a
`Lookaround(direction=BEHIND)` containing a `GroupReference` will
therefore always be rejected by Point 3's check, which is correct:
Python's `re` rejects exactly this case too.
"""
