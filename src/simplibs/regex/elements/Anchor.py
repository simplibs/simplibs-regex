# Outers
from ..base_class import Regex
# Inners
from .enums import AnchorKind
from ._validations import raise_anchor_invalid_kind_error


class Anchor(Regex):
    """Zero-width position assertion — matches a position, not a character.

    Pattern:
        ^ $ \\A \\Z \\b \\B  (depending on `kind`)

    Example:
        Anchor(AnchorKind.START_STRING)   # -> "\\A"
        START                             # preset, see presets/anchors.py
    """

    __slots__ = ("kind",)

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, kind: AnchorKind) -> None:

        # 1. Parameter validation
        if not isinstance(kind, AnchorKind):
            raise_anchor_invalid_kind_error(kind)

        # 2. Parameter assignment
        self.kind = kind

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Every AnchorKind value IS its own regex fragment.
        return self.kind.value

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every anchor is zero-width by definition — always fixed at 0,
        #    and always safe inside a lookbehind (a zero-width assertion
        #    inside another zero-width assertion is unusual but valid).
        return 0


_DESIGN_NOTES = """
# Anchor — Zero-Width Position Assertion Atom

## One class, one enum — not six classes
Mirrors the `Repeat`/`Group` decision from the mechanism review: six
syntaxes (`^ $ \\A \\Z \\b \\B`) collapse to one parameterized class plus
an enum, exactly the pattern `CharacterType` will also follow for
`\\d \\D \\w \\W \\s \\S`. The public-facing presets (`START`, `END`,
`START_STRING`, `WORD_BOUNDARY`, ...) are plain module-level `Anchor(...)`
instances built once in `presets/anchors.py` — see that file once it
exists.

## `\\z` intentionally omitted from AnchorKind for now
The raw catalog (konverzace 4) notes `\\z` as a Python 3.14 addition,
with `\\Z` documented as now equivalent to it. Since this library's
target Python floor is not yet pinned to 3.14+, `END_STRING` maps to
`\\Z` (available on every supported version) rather than `\\z`. Revisit
once the library's minimum Python version is decided — if it lands on
3.14+, `\\z` can be added as its own `AnchorKind` member (or `END_STRING`
can be repointed to it) without breaking anything already built on top,
since callers only ever see the `END_STRING` name, never the literal
escape sequence.

## `fixed_length` is unconditionally 0
Not a simplification — every anchor, by the definition of "zero-width
assertion", consumes no characters no matter what it matches against.
This is the one node type in the whole tree where `fixed_length` never
needs a conditional; it is always safe, unlike `Sequence`/`Alternation`/
`Repeat`, whose fixed length depends on their children.
"""
