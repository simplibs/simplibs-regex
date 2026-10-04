# Outers
from ..base_class import Regex, Precedence
# Inners
from .enums import RepeatMode
from ._validations import (
    raise_repeat_inner_not_repeatable_error,
    raise_repeat_min_negative_error,
    raise_repeat_max_less_than_min_error,
    raise_param_invalid_type_error
)


class Repeat(Regex):
    """Repeat the inner node between `min` and `max` times.

    Unifies all 14 Python `re` quantifier syntaxes — `*` `+` `?` `{n}`
    `{n,}` `{m,n}`, each in greedy/lazy/possessive form — into one
    parameterized mechanism.

    Pattern:
        A*, A+, A?, A{n}, A{n,}, A{m,n}  (+ trailing `?`/`+` for mode)

    Example:
        Repeat(DIGIT, min=0, max=None)                    # -> "\\d*"
        Repeat(DIGIT, min=1, max=None, mode=RepeatMode.LAZY)   # -> "\\d+?"
        Repeat(Literal("ab"), min=3, max=3)                # -> "(?:ab){3}"
    """

    __slots__ = ("inner", "min", "max", "mode")

    _precedence = Precedence.REPEAT

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        inner: Regex,
        *,
        min: int = 0,
        max: int | None = None,
        mode: RepeatMode = RepeatMode.GREEDY,
    ) -> None:

        # 1. Parameter validation — types (bool is a subclass of int, so it is excluded explicitly)
        if not isinstance(inner, Regex):
            raise_param_invalid_type_error("inner", inner)
        if isinstance(min, bool) or not isinstance(min, int):
            raise_param_invalid_type_error("min", min)
        if max is not None and (isinstance(max, bool) or not isinstance(max, int)):
            raise_param_invalid_type_error("max", max)
        if not isinstance(mode, RepeatMode):
            raise_param_invalid_type_error("mode", mode)

        # 2. Parameter validation — `re` rejects a quantifier right after some nodes (an Anchor)
        if not inner._repeatable:
            raise_repeat_inner_not_repeatable_error(inner)

        # 3. Parameter validation — minimum repetition count cannot be negative
        if min < 0:
            raise_repeat_min_negative_error(min)

        # 4. Parameter validation — maximum repetition count cannot be less than minimum
        if max is not None and max < min:
            raise_repeat_max_less_than_min_error(min, max)

        # 5. Parameter assignment
        self.inner = inner
        self.min = min
        self.max = max
        self.mode = mode

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. A quantifier binds to exactly ONE preceding unit, so the inner
        #    node is rendered at ATOM precedence: anything looser (Sequence,
        #    Alternation, and another Repeat — `a*{3}` is invalid) gets
        #    wrapped in (?:...) by `render`.
        inner_pattern = self.inner.render(Precedence.ATOM)

        # 2. An ATOM-precedence child that is NOT a single
        #    quantifiable token (a multi-character Literal) still needs
        #    an explicit wrap, which the precedence comparison in step 1
        #    could not have added on its own.
        if self.inner.needs_wrap_for_repeat():
            inner_pattern = f"(?:{inner_pattern})"

        # 3. Build the quantifier suffix from min/max.
        quantifier = self._build_quantifier()

        # 4. Append the mode suffix (empty for greedy, "?" for lazy,
        #    "+" for possessive).
        return f"{inner_pattern}{quantifier}{self.mode.value}"

    def _build_quantifier(self) -> str:
        """Choose the shortest correct `re` quantifier syntax for
        (self.min, self.max), collapsing to `*`/`+`/`?` where possible
        rather than always emitting the general `{m,n}` form."""

        # 1. The three single-character shorthands.
        if self.min == 0 and self.max is None:
            return "*"
        if self.min == 1 and self.max is None:
            return "+"
        if self.min == 0 and self.max == 1:
            return "?"

        # 2. Exact count.
        if self.min == self.max:
            return f"{{{self.min}}}"

        # 3. Open-ended minimum.
        if self.max is None:
            return f"{{{self.min},}}"

        # 4. General bounded range.
        return f"{{{self.min},{self.max}}}"

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Zero repetitions always match an empty string, regardless of
        #    what the inner node's own length would otherwise be.
        if self.min == 0 and self.max == 0:
            return 0

        # 2. A fixed length is only knowable when the repeat count itself
        #    is exact (min == max) AND the inner node has a fixed length.
        if self.min != self.max:
            return None

        inner_length = self.inner.fixed_length()
        if inner_length is None:
            return None

        return self.min * inner_length


_DESIGN_NOTES = """
# Repeat — Unified Quantifier Mechanism

## The 14-to-1 collapse
`*` `+` `?` `{n}` `{n,}` `{m,n}`, each in greedy/lazy/possessive form,
are all one mechanism: a min/max count plus a backtracking mode. Nothing
about them differs structurally — `_build_quantifier` recovers the
shorthand syntax purely as an OUTPUT optimization (`*` reads better than
`{0,}`), never as a distinct code path with its own class.

## Why min/max are plain ints/None instead of their own tiny value object
Every other simplibs container (`AllOf`, `Sequence`) takes its
parameters as directly as possible; `Repeat`'s min/max map onto Python's
own `int | None` idiom for "unbounded" cleanly enough that a dedicated
wrapper type would add indirection without adding safety — the
validation in `__init__` (min >= 0, max >= min) already catches the
only two ways these two values can be mutually invalid.

## `RepeatMode` as an Enum, not three boolean flags
`lazy: bool` and `possessive: bool` as two separate flags would allow
the nonsensical `lazy=True, possessive=True` (Python's `re` has no
"lazy possessive" quantifier) to be constructed and only fail — if it
failed at all — deep inside `to_pattern`. A three-member `Enum` makes
the invalid combination unrepresentable in the type system itself,
consistent with `AnchorKind`/`CharacterTypeKind`'s own enum choice for
the same reason.

## The `needs_wrap_for_repeat` check, concretely
`Repeat(Literal("ab"), min=3, max=3).to_pattern()` must produce
`(?:ab){3}`, not `ab{3}` (which would only repeat the final `b`).
Step 1 (`inner.render(Precedence.ATOM)`) does NOT add this wrap on its
own — `Literal`'s `_precedence` is ATOM, which is not lower than
ATOM, so the ordinary precedence comparison in `Regex.render` sees no
reason to wrap it. Step 2 is exactly the escape hatch `Regex.
needs_wrap_for_repeat` exists for for this one case; every other
ATOM-precedence node's default `False` means step 2 is a no-op for
`Anchor`, `CharacterType`, `Group`, `CharacterClass`, `Lookaround`, and
`GroupReference` alike.

## Why the inner node renders at ATOM, not at REPEAT
Rendering at Repeat's own level (REPEAT) would leave a nested `Repeat`
unwrapped, producing `a*{3}` (or `a**`) — which `re` rejects as
"multiple repeat". ATOM makes every non-single-token child
(Sequence, Alternation, Repeat) wrap itself: `(?:a*){3}`.

## Why an Anchor is refused as `inner`
`^*`, `\\b?`, `\\A?` and `a\\Z*` fail in `re` with "nothing to repeat". The node
flag `_repeatable` (False on `Anchor`) lets `Repeat` say so at construction time.
Only the bare node is refused: a lookaround or a `Group` around an anchor is
accepted by `re`, so they stay legal.

## `fixed_length` — the {0} special case
`Repeat(anything, min=0, max=0)` always matches the empty string,
independent of whatever `self.inner.fixed_length()` would otherwise
report (even if the inner node itself has variable/unknown length,
`{0}` around it is still fixed at exactly 0). This is checked BEFORE the
general `min == max` branch precisely so it never depends on the inner
node's own introspection succeeding.
"""
