# Outers
from ..base_class import Regex, Precedence
# Inners
from ._validations import (
    raise_group_reference_numeric_out_of_range_error,
    raise_group_reference_invalid_identifier_error,
    raise_group_reference_invalid_type_error,
)


class GroupReference(Regex):
    """Backreference to a previously captured group, by number or name.

    Pattern:
        \\1              id_or_name is an int (1-99)
        (?P=name)        id_or_name is a str

    Example:
        GroupReference(1)          # -> "\\1"
        GroupReference("year")     # -> "(?P=year)"

    A numeric reference embedded in a Sequence or Repeat is rendered as
    "(?:\\1)", so a following digit can never merge into its number.
    """

    __slots__ = ("id_or_name",)

    # Deliberately left at the base class default (False): `\1` inside a
    # CharacterClass is an OCTAL escape, not a backreference — the two
    # contexts mean genuinely different things, so a GroupReference is
    # never a legal CharacterClass item (unlike CharacterType/CharacterCode,
    # where the meaning is identical either side of `[...]`).

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        id_or_name: int | str
    ) -> None:

        # 1. Parameter validation — type (bool is a subclass of int, so it is excluded explicitly)
        if isinstance(id_or_name, bool) or not isinstance(id_or_name, (int, str)):
            raise_group_reference_invalid_type_error(id_or_name)

        # 2. Parameter validation — numeric range check for integer references
        if isinstance(id_or_name, int):
            if not (_MIN_GROUP_NUMBER <= id_or_name <= _MAX_GROUP_NUMBER):
                raise_group_reference_numeric_out_of_range_error(
                    id_or_name, _MIN_GROUP_NUMBER, _MAX_GROUP_NUMBER
                )

        # 3. Parameter validation — identifier check for named references
        elif not id_or_name.isidentifier():
            raise_group_reference_invalid_identifier_error(id_or_name)

        # 4. Parameter assignment
        self.id_or_name = id_or_name

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Numeric id -> \1 syntax; name -> (?P=name) syntax.
        if isinstance(self.id_or_name, int):
            return f"\\{self.id_or_name}"
        return f"(?P={self.id_or_name})"

    # ----------------------------------------------------------------------
    # Embedding-aware rendering (see Regex.render)
    # ----------------------------------------------------------------------
    def render(self, parent_precedence: Precedence) -> str:

        # 1. A numeric reference followed by a digit would merge into a
        #    different number (`\1` + `0` -> `\10`). Inside a Sequence or
        #    Repeat the next sibling is unknown, so it is always wrapped.
        #    A named reference ends in ")" and never needs this.
        fragment = self.to_pattern()
        if isinstance(self.id_or_name, int) and parent_precedence >= Precedence.SEQUENCE:
            return f"(?:{fragment})"
        return fragment

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Genuinely unknowable in general — a backreference's match
        #    width depends entirely on whatever text the referenced
        #    group actually captured at runtime, which this static tree
        #    has no way to know (the referenced Group node isn't even
        #    reachable from here — GroupReference stores only an id/name,
        #    not a pointer back to the Group it refers to).
        return None


# Python's `re` reads `\100` and above as an octal escape, so a numbered
# backreference can only address groups 1 to 99.
_MIN_GROUP_NUMBER = 1
_MAX_GROUP_NUMBER = 99


_DESIGN_NOTES = """
# GroupReference — Numeric and Named Backreferences

## Why it is never usable inside a CharacterClass
This is the sharpest example in the whole library: `\\1`
OUTSIDE a character class is a backreference, but `\\1` INSIDE `[...]`
is an octal escape (character code 1) — genuinely different meanings for
the identical text. Leaving `_usable_in_char_class` at its base-class
`False` default (rather than needing a special-case check anywhere)
is exactly what that flag exists to prevent: silently reusing a
`GroupReference` where its rendered text would mean something entirely
different.

## Why numeric ids are limited to 1-99
Python's `re` reads `\\1` to `\\99` as backreferences, but a three-digit
`\\100` or higher as an OCTAL escape (`\\100` matches "@"). Allowing
100 would silently build a different pattern than the one described, so
it is rejected at construction. A group beyond 99 can still be addressed
by giving the Group a name and using `GroupReference("name")`, which has
no limit.

## Why `bool` is rejected
`True` and `False` are `int` instances in Python, so a plain type check
would accept them and render the nonsense fragment `\\True`. They are
refused explicitly as an invalid type.

## Why a numeric reference is wrapped when embedded
`GroupReference(1)` followed by the literal "0" would render `\\10`,
which `re` reads as group 10 — either a compile error or, worse, a
silent reference to a different group. A node cannot see its next
sibling, so `render` always wraps a numeric reference in `(?:...)` when
the parent is a `Sequence` or `Repeat`. Standalone, and inside an
`Alternation`, `Group` or `Lookaround` (which delimit it themselves), it
stays a bare `\\1`. A named reference ends in `)` and never needs this.

## Why the existence of the group is NOT checked here
`GroupReference` stores only an id or name, not a pointer to the Group.
Whether such a group exists (and is defined before the reference) is a
property of the whole tree, which only `RegexPattern` sees. A dangling
reference therefore surfaces there, as the structured invalid-pattern
error, rather than here.

## Why `fixed_length` is unconditionally None
Unlike `Anchor`/`CharacterType` (always genuinely 0 or 1), a
backreference's width is a real runtime unknown from a static tree's
point of view — it depends on what the referenced group actually
matched. Returning `None` is the only honest answer; a
`Lookaround(direction=BEHIND)` containing a `GroupReference` will
therefore always be rejected by check, which is correct:
Python's `re` rejects exactly this case too.
"""