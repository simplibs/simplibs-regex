# Outers
from ..base_class import Regex, Precedence
# Inners
from .enums import LookaroundDirection
from ._validations import (
    raise_variable_length_lookbehind_error,
    raise_param_invalid_type_error
)


class Lookaround(Regex):
    """Zero-width assertion that `inner` does (or does not) match at the
    current position, without consuming any characters.

    Unifies all 4 Python `re` lookaround syntaxes into one parameterized
    mechanism, the same way `Repeat` and `Group` unify their own
    syntax families.

    Pattern:
        (?=A)    direction=AHEAD,  negate=False
        (?!A)    direction=AHEAD,  negate=True
        (?<=A)   direction=BEHIND, negate=False
        (?<!A)   direction=BEHIND, negate=True

    Example:
        Lookaround(DIGIT, direction=LookaroundDirection.AHEAD)         # -> "(?=\\d)"
        Lookaround(Literal("USD"), direction=LookaroundDirection.BEHIND)  # -> "(?<=USD)"

    Constructing a BEHIND lookaround whose `inner` has no fixed length
    raises immediately, instead of letting Python's `re` reject it later
    at `re.compile()` with a less specific error.
    """

    __slots__ = ("inner", "direction", "negate")

    # Self-delimiting via its own (?=...)/(?<=...) syntax — stays at the
    # base class ATOM default, same reasoning as Group/CharacterClass.

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        inner: Regex,
        *,
        direction: LookaroundDirection,
        negate: bool = False,
    ) -> None:

        # 1. Parameter validation — types
        if not isinstance(inner, Regex):
            raise_param_invalid_type_error("inner", inner)
        if not isinstance(direction, LookaroundDirection):
            raise_param_invalid_type_error("direction", direction)
        if not isinstance(negate, bool):
            raise_param_invalid_type_error("negate", negate)

        # 2. Fail fast on a variable-length lookbehind, rather
        #    than deferring to re.compile()'s own, less specific error.
        if direction is LookaroundDirection.BEHIND and inner.fixed_length() is None:
            raise_variable_length_lookbehind_error(inner)

        # 3. Parameter assignment
        self.inner = inner
        self.direction = direction
        self.negate = negate

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. This node's own parentheses already delimit `inner`
        #    completely — render at the loosest precedence, same
        #    reasoning as Group.to_pattern.
        inner_pattern = self.inner.render(Precedence.ALTERNATION)

        prefix = self._build_prefix()
        return f"{prefix}{inner_pattern})"

    def _build_prefix(self) -> str:
        """Return the opening syntax for this specific direction/negate combination."""

        if self.direction is LookaroundDirection.AHEAD:
            return "(?!" if self.negate else "(?="

        return "(?<!" if self.negate else "(?<="

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every lookaround is zero-width by definition — it asserts
        #    something about neighboring text without consuming it,
        #    exactly like Anchor.
        return 0


_DESIGN_NOTES = """
# Lookaround — Unified Assertion Mechanism

## The 4-to-1 collapse
`(?=A)` `(?!A)` `(?<=A)` `(?<!A)` are one mechanism: a direction plus a
negate flag, exactly the same "small closed set of modifiers on one
inner node" shape as `Group`'s six variants and `Repeat`'s three modes.

This is the payoff of `fixed_length` existing on `Regex` at all: step 3
of `__init__` calls `inner.fixed_length()` and rejects `None` immediately
when `direction is BEHIND`. Every `fixed_length` override written so
far — `Literal` (exact), `Anchor`/`CharacterType`/`CharacterClass`
(constant), `Sequence` (sum, or `None` on the first variable child),
`Alternation` (shared length or `None`), `Repeat` (only when
`min == max`), `Group` (transparent delegation) — exists specifically so
this one check has an honest answer to work with. A caller building
`Lookaround(ZERO_OR_MORE(DIGIT), direction=BEHIND)` gets a clear,
specific `ValueError` naming exactly what went wrong, at the exact line
that tried to construct it — never a cryptic failure three layers away
inside `re.compile()`.

## Why AHEAD lookarounds never call `fixed_length` at all
Only `direction is BEHIND` triggers the check — `re` has no
fixed-length requirement for lookahead, since a lookahead is evaluated
left-to-right just like the rest of the pattern and never needs to know
its own width in advance. Skipping the check entirely for AHEAD avoids
an unnecessary `fixed_length()` call (and the tree walk it can trigger
on a large `inner`) in the common case where it can never matter.

## `to_pattern` renders `inner` at ALTERNATION precedence
Identical reasoning to `Group.to_pattern`: the lookaround's own
parentheses are already a hard delimiter, so `inner` never needs an
extra wrap from `render`'s ordinary precedence comparison — rendering
at the loosest level (ALTERNATION) guarantees no redundant double-wrap.

## `fixed_length` is unconditionally 0
Same shape as `Anchor` — a lookaround, like any zero-width assertion,
consumes no characters regardless of what its own `inner` matches
against. This makes a `Lookaround` itself always safely embeddable
inside a further outer `Lookaround(direction=BEHIND)`, without needing
any special-casing.
"""
