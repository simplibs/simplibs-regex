import sys
# Outers
from ..base_class import Regex
# Inners
from .enums import AnchorKind
from ._validations import (
    raise_anchor_requires_python_314_error,
    raise_param_invalid_type_error
)

# `\z` (AnchorKind.END_STRING_PY314) exists only from this version on.
_PY314 = (3, 14)


class Anchor(Regex):
    """Zero-width position assertion — matches a position, not a character.

    Pattern:
        ^ $ \\A \\Z \\z \\b \\B  (depending on `kind`)

    Example:
        Anchor(AnchorKind.START_STRING)   # -> "\\A"
        START                             # preset, see presets/anchors.py
    """

    __slots__ = ("kind",)

    # `re` rejects a quantifier placed directly on an anchor (`^*`, `\\b?` ->
    # "nothing to repeat"); `Repeat` reads this flag at construction time.
    _repeatable = False

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        kind: AnchorKind
    ) -> None:

        # 1. Parameter validation — type
        if not isinstance(kind, AnchorKind):
            raise_param_invalid_type_error(
                "kind", "an AnchorKind member", kind, "AnchorKind.START_STRING"
            )

        # 2. Parameter validation — `\\z` needs Python 3.14+
        if kind is AnchorKind.END_STRING_PY314 and sys.version_info < _PY314:
            raise_anchor_requires_python_314_error()

        # 3. Parameter assignment
        self.kind = kind

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Every AnchorKind value IS its own regex fragment.
        return self.kind.value

    # ----------------------------------------------------------------------
    # Fixed-length introspection
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

## `\\z` and the Python version guard
`\\z` (end of the whole string, identical in meaning to `\\Z`) exists
only on Python 3.14+. It is its own member, `END_STRING_PY314`, and
`__init__` rejects it on older interpreters with a message pointing at
`END_STRING` — instead of letting `re.compile` fail later with a bare
`bad escape \\z`. `END_STRING` stays `\\Z`, which works on every
supported version.

## Never directly repeatable
`^*`, `\\b?`, `\\A?` and `a\\Z*` all fail in `re` with "nothing to repeat",
so `_repeatable = False` lets `Repeat` refuse an anchor at construction time
instead of at compile time. Wrapped in a `Group` the same anchor is accepted.

## `fixed_length` is unconditionally 0
Not a simplification — every anchor, by the definition of "zero-width
assertion", consumes no characters no matter what it matches against.
This is the one node type in the whole tree where `fixed_length` never
needs a conditional; it is always safe, unlike `Sequence`/`Alternation`/
`Repeat`, whose fixed length depends on their children.
"""
