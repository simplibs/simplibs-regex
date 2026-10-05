# Outers
from ..base_class import Regex
# Inners
from .enums import CharacterTypeKind
from ._validations import raise_param_invalid_type_error


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

    # One of the few node types whose meaning is IDENTICAL
    # inside and outside a CharacterClass, so it is always a legal item.
    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        kind: CharacterTypeKind
    ) -> None:

        # 1. Parameter validation — type
        if not isinstance(kind, CharacterTypeKind):
            raise_param_invalid_type_error(
                "kind", "a CharacterTypeKind member", kind, "CharacterTypeKind.DIGIT"
            )

        # 2. Parameter assignment
        self.kind = kind

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Every CharacterTypeKind value IS its own regex fragment.
        return self.kind.value

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every built-in character type matches exactly one character.
        return 1


_DESIGN_NOTES = """
# CharacterType — Built-in Character Class Atom

## One class, one enum — same shape as Anchor
`\\d \\D \\w \\W \\s \\S` collapse into one parameterized class, exactly
the pattern used for `Anchor`. Presets (`DIGIT`, `NON_DIGIT`, `WORD_CHARACTER`,
...) are plain instances in `presets/character_types.py`.

## Why this is the one atom type usable in a CharacterClass unchanged
Whole premise — escape sequences meaning something different
inside `[...]` than outside it — genuinely does NOT apply to
`\\d \\D \\w \\W \\s \\S`: Python's `re` documentation is explicit that
these six retain their outside-the-class meaning when placed inside one
(`[\\d\\s]` really does mean "a digit or a whitespace character"). That
is precisely why `_usable_in_char_class` is unconditionally `True` here,
with no length-based caveat the way `Literal` needs one — there is no
case where a `CharacterType` means something different or illegal
inside a `CharacterClass`.
"""
