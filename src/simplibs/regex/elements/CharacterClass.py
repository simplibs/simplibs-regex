# Outers
from ..base_class import Regex
from .Literal import Literal
# Inners
from ._validations import (
    raise_character_class_empty_error,
    raise_character_class_item_not_allowed_error,
    raise_multi_character_literal_in_char_class_error,
)


class CharacterClass(Regex):
    """Match exactly one character, chosen from (or excluded from) the
    given set of items.

    Pattern:
        [items]     negate=False
        [^items]    negate=True

    Only accepts items where `_usable_in_char_class` is `True` — a
    single-character `Literal`, a `CharacterType` (`DIGIT`, `WORD_CHARACTER`, ...),
    a `CharacterRange`, or a `CharacterCode`. This is enforced at
    construction time: escape semantics differ inside `[...]`, so only
    nodes that know how to render themselves correctly in that context
    (via `to_char_class_fragment`) are ever allowed in.

    Example:
        CharacterClass(Literal("a"), Literal("b"), Literal("c"))  # -> "[abc]"
        CharacterClass(CharacterRange("a", "z"), negate=True)      # -> "[^a-z]"
        CharacterClass(DIGIT, WHITESPACE)                          # -> "[\\d\\s]"
    """

    __slots__ = ("items", "negate")

    # A CharacterClass is always self-delimiting via its own `[...]` —
    # stays at the base class ATOM default, same reasoning as Group.

    # Python's `re` does not support nesting one character class inside
    # another, so a CharacterClass is never itself a legal item of
    # another CharacterClass — stays at the base class False default.

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        *items: Regex,
        negate: bool = False
    ) -> None:

        # 1. Parameter validation — at least one item
        if not items:
            raise_character_class_empty_error()

        # 2. Parameter validation — every item must be a Regex node
        #    explicitly opted into character-class usage.
        for item in items:
            if not isinstance(item, Regex) or not item._usable_in_char_class:
                raise_character_class_item_not_allowed_error(item)
            if isinstance(item, Literal) and len(item.text) != 1:
                raise_multi_character_literal_in_char_class_error(item.text)

        # 3. Parameter assignment
        self.items: tuple[Regex, ...] = items
        self.negate = negate

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Every item renders via its character-class-specific
        #    fragment method, never via to_pattern() directly —
        #    that is exactly the distinction to_char_class_fragment
        #    exists to make.
        content = "".join(item.to_char_class_fragment() for item in self.items)
        prefix = "[^" if self.negate else "["
        return f"{prefix}{content}]"

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. A character class always matches exactly one character,
        #    unconditionally — regardless of how many items it contains
        #    or what they are.
        return 1


_DESIGN_NOTES = """
# CharacterClass — Enforced at Construction Time

## Where the actual validation lives
`__init__` is the single enforcement point: every item must
be a `Regex` instance with `_usable_in_char_class = True`, checked via
`isinstance` + attribute check — deliberately the same procedural-check
shape `Rule.__and__` already uses for `__not_rule__`, as flagged back in
`Regex`'s own design notes as the intentional choice over a fully
separate type hierarchy. A `Literal` additionally gets its OWN,
length-specific check here (`len(item.text) != 1`), because
`_usable_in_char_class` is a per-CLASS flag and cannot express a
per-INSTANCE constraint — a `Literal("a")` is fine, a `Literal("ab")` is
not, and only `CharacterClass.__init__` has the actual instance in hand
to tell the two apart.

## Why rendering calls `to_char_class_fragment`, never `to_pattern`
This is the concrete payoff of the hook added to `Regex`/`Literal`
earlier: `CharacterType`/`CharacterRange`/`CharacterCode` items render
identically either way (their `to_char_class_fragment` just delegates
to `to_pattern` via the base class default), but a `Literal` item
renders through its OWN override, which escapes only `] ^ - \\` instead
of the full `re.escape` set `Literal.to_pattern` uses outside a class.
Calling `to_pattern()` here by mistake would still often produce a
technically-valid class (over-escaping inside `[...]` is harmless), but
would violate the design intent of having each context use its own
correct, minimal escaping.

## Why `fixed_length` is unconditionally 1
Same shape of reasoning as `Anchor.fixed_length` being unconditionally
0: a character class, by definition, matches exactly one character
regardless of how many alternatives it offers or whether it is negated.
No child inspection is needed at all here — unlike `Sequence`/`Repeat`,
which must ask their children.

## No nesting — deliberately not revisited here
Python's `re` does not support a `CharacterClass` containing another
`CharacterClass` (the raw catalog's konverzace 4 flags this explicitly
as a documented non-feature, not an oversight). `CharacterClass` simply
never sets `_usable_in_char_class = True` on itself, so attempting
`CharacterClass(CharacterClass(...))` is rejected by the ordinary item
check above with no special-case code needed for the nested case.
"""
