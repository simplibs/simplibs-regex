import re
# Outers
from ..base_class import Regex
# Inners
from ._helpers import escape_char_class_char
from ._validations import (
    raise_literal_empty_error,
    raise_literal_not_single_char_error,
    raise_param_invalid_type_error
)


class Literal(Regex):
    """Match the given text literally, character for character.

    Pattern:
        the text, with every regex-special character auto-escaped

    Example:
        Literal("a.b")      # -> "a\\.b" (matches the literal string "a.b")
        Literal("3+3=6")    # -> "3\\+3=6"
    """

    __slots__ = ("text",)

    # _precedence stays at the base class default (ATOM): a single
    # rendered literal is already self-delimiting — see caveat below on
    # multi-character literals and Repeat.

    # A Literal is only usable inside a CharacterClass when it
    # is exactly one character wide; CharacterClass itself enforces the
    # length at the point of use (see its own validation), since a
    # class-level flag can't express "sometimes, depending on content".
    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        text: str
    ) -> None:

        # 1. Parameter validation — type
        if not isinstance(text, str):
            raise_param_invalid_type_error(
                "text", "a str", text, 'Literal("abc")'
            )

        # 2. Parameter validation — literal text cannot be empty
        if text == "":
            raise_literal_empty_error()

        # 3. Parameter assignment
        self.text = text

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Escape every regex-special character in the literal text.
        return re.escape(self.text)

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. A literal always matches exactly len(text) characters,
        #    regardless of escaping (re.escape never changes how many
        #    source characters are consumed at match time).
        return len(self.text)

    # ----------------------------------------------------------------------
    # Repeat-wrapping hook
    # ----------------------------------------------------------------------
    def needs_wrap_for_repeat(self) -> bool:

        # 1. A quantifier binds to exactly one token — only a
        #    single-character literal already qualifies on its own.
        return len(self.text) > 1

    # ----------------------------------------------------------------------
    # Character-class rendering hook
    # ----------------------------------------------------------------------
    def to_char_class_fragment(self) -> str:

        # 1. Defensive assertion — single-character check for character class fragment
        if len(self.text) != 1:
            raise_literal_not_single_char_error(self.text)

        # 2. Character-class escaping only cares about a different,
        #    smaller set of specials than general-purpose re.escape.
        return escape_char_class_char(self.text)


_DESIGN_NOTES = """
# Literal — Literal Text Atom

## Why `_precedence` is left at the ATOM default, with a caveat
A single `Literal("abc")` rendered on its own is self-delimiting the
same way any atom is — nothing needs to wrap it. The caveat lives on the
CONSUMING side, not here: `Repeat` binds to exactly one preceding
"unit", and a multi-character `Literal` is NOT one unit in that sense
(`Repeat(Literal("ab"), min=3, max=3)` must render as `(?:ab){3}`, not `ab{3}`,
or the repeat would apply only to the final `b`). This is intentionally
NOT solved by lowering `Literal`'s own `_precedence` — a `Literal` is
still correctly unwrapped when embedded in a `Sequence` or
`Alternation`, where per-character binding is irrelevant. It is `Repeat`
itself that must special-case multi-character literals when deciding
whether to wrap its inner node; see `Repeat.py`'s own design notes for
exactly how (`Repeat` asks the dedicated `needs_wrap_for_repeat()` hook,
because `Precedence` alone cannot express "binds to one character" as
a level).

## Why empty string is rejected
An empty `Literal` would render as `""` — silently invisible inside a
`Sequence`, and actively meaningless as a standalone node (what would
`Literal("") | Literal("x")` even communicate to a reader?). Rejecting
it at construction time is consistent with `Contains`'s own non-empty
substring convention in `simplibs-rules`, and avoids a silent no-op
node anywhere in a composed tree.

## Why escaping happens in `to_pattern`, not at construction time
`self.text` is kept as the ORIGINAL, unescaped string — useful for any
future introspection/debugging (`repr`, tooling that wants to know what
literal text a node represents) exactly the same rationale `IsTyping`
gives for storing `self.annotation` even though `self.rule` does the
real work. Escaping is a pure rendering concern, recomputed in
`to_pattern` from the one source of truth.

## `_usable_in_char_class` is always True, length checked by the consumer
A `Literal` is always a legal single item — or (for multi-character
input) an explicit list of items — inside a `CharacterClass`, but a
CharacterClass is a set of individual characters, not a substring
match: `[ab]` means "a or b", never "the string ab". Rather than
rejecting multi-character literals here (which would make `Literal`
context-dependent on where it's about to be used — a `Regex` node has
no way to know that ahead of time), the flag stays a simple opt-in and
`CharacterClass.__init__` is the one place that actually inspects
`len(item.text)` for any `Literal` item it receives, raising there if
it isn't exactly one character. See `CharacterClass.py`'s own design
notes.
"""
