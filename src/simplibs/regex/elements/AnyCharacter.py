# Outers
from ..base_class import Regex


class AnyCharacter(Regex):
    """Match any single character.

    Pattern:
        .

    Example:
        AnyCharacter()                          # -> "."
        ANY                                     # preset, see presets/any_character.py
        Literal("a") + AnyCharacter() + Literal("c")   # -> "a.c"

    Without the DOTALL flag it does not match a newline; with DOTALL it
    matches truly any character. The flag belongs to the whole pattern
    (see Flag, RegexPattern), never to this node.
    """

    __slots__ = ()

    # NEVER usable inside a CharacterClass: `[.]` means the
    # LITERAL character ".", not "any character". Rejecting it at
    # construction is safer than silently compiling a different meaning.
    _usable_in_char_class = False

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. The wildcard is always the same single dot.
        return "."

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Exactly one character, with or without DOTALL.
        return 1


_DESIGN_NOTES = """
# AnyCharacter — The `.` Wildcard Atom

## Why this is its own class and not a CharacterTypeKind member
`\\d \\D \\w \\W \\s \\S` are real character classes and keep their
meaning inside `[...]`. The dot does not: `[.]` is a literal dot. If
`.` lived in `CharacterTypeKind`, `CharacterType` (which is always
usable in a `CharacterClass`) would let `CharacterClass(ANY, DIGIT)`
compile silently to `[.\\d]` — a different meaning than the caller
intended. A separate class can state `_usable_in_char_class = False`
honestly, and `CharacterClass` rejects it at construction.

## Why it has no parameters
There is exactly one wildcard, so there is no Kind enum and no
validation. The preset `ANY` is a plain instance of this class.

## Why newline behaviour is not modelled here
Whether `.` matches a newline depends on the DOTALL flag of the whole
pattern (or of an enclosing scoped Group), not on the node. The node
renders the same `.` either way and always consumes one character.
"""