# Outers
from ..base_class import Regex
# Inners
from .enums import CharacterTypeKind
from ._validations import raise_character_type_invalid_kind_error


class CharacterType(Regex):
    """A single character matching a built-in Unicode character class.

    Pattern:
        \\d \\D \\w \\W \\s \\S  (depending on `kind`)

    Example:
        CharacterType(CharacterTypeKind.DIGIT)   # -> "\\d"
        DIGIT                                     # preset, see presets/character_types.py

    Also legal as a standalone item inside a CharacterClass, e.g.
    CharacterClass(DIGIT, WHITESPACE) -> "[\\d\\s]" — the escape sequence
    means exactly the same thing inside `[...]` as outside it, unlike
    most other escapes (see CharacterClass's own design notes).
    """

    __slots__ = ("kind",)

    # Point 4 — one of the few node types whose meaning is IDENTICAL
    # inside and outside a CharacterClass, so it is always a legal item[cite: 27].
    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, kind: CharacterTypeKind) -> None:

        # 1. Parameter validation
        if not isinstance(kind, CharacterTypeKind):
            raise_character_type_invalid_kind_error(kind)

        # 2. Parameter assignment
        self.kind = kind

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Every CharacterTypeKind value IS its own regex fragment[cite: 27].
        return self.kind.value

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every built-in character type matches exactly one character[cite: 27].
        return 1


_DESIGN_NOTES = """
# CharacterType — Built-in Character Class Atom

## One class, one enum — same shape as Anchor
`\\d \\D \\w \\W \\s \\S` collapse into one parameterized class, exactly
the pattern used for `Anchor`. Presets (`DIGIT`, `NON_DIGIT`, `WORD`,
...) are plain instances in `presets/character_types.py`.

## Why this is the one atom type usable in a CharacterClass unchanged
Point 4's whole premise — escape sequences meaning something different
inside `[...]` than outside it — genuinely does NOT apply to
`\\d \\D \\w \\W \\s \\S`: Python's `re` documentation is explicit that
these six retain their outside-the-class meaning when placed inside one
(`[\\d\\s]` really does mean "a digit or a whitespace character"). That
is precisely why `_usable_in_char_class` is unconditionally `True` here,
with no length-based caveat the way `Literal` needs one — there is no
case where a `CharacterType` means something different or illegal
inside a `CharacterClass`.
"""
