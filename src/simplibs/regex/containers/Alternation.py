# Outers
from ..base_class import Regex, _Precedence
# Inners
from ._validations import (
    raise_requires_at_least_one_node_error,
    raise_node_param_not_regex_error,
)


class Alternation(Regex):
    """Match any ONE of the given nodes.

    Pattern:
        A|B|...

    Example:
        Alternation(Literal("cat"), Literal("dog"))   # -> "cat|dog"
        Literal("cat") | Literal("dog")                # same, via operator sugar
    """

    __slots__ = ("nodes",)

    _precedence = _Precedence.ALTERNATION

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, *nodes: Regex) -> None:

        # 1. Parameter validation
        if not nodes:
            raise_requires_at_least_one_node_error("Alternation")

        # 2. Flatten nested Alternation instances (e.g. from `a | b | c`
        #    chaining) into a single flat node list, rather than nesting
        #    Alternation(Alternation(...), ...)
        flattened: list[Regex] = []
        for node in nodes:
            if not isinstance(node, Regex):
                raise_node_param_not_regex_error("Alternation", node)
            if type(node) is Alternation:
                node: Alternation
                flattened.extend(node.nodes)
            else:
                flattened.append(node)

        # 3. Parameter assignment
        self.nodes: tuple[Regex, ...] = tuple(flattened)

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Render every child against THIS node's own precedence, then
        #    join with "|". A branch that is itself an Alternation never
        #    occurs here (flattened away in __init__); a branch that is a
        #    Sequence renders unwrapped, since SEQUENCE > ALTERNATION.
        return "|".join(node.render(self._precedence) for node in self.nodes)

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. An alternation has a fixed length only if EVERY branch has
        #    the SAME fixed length (Python's `re` does accept this shape
        #    inside a lookbehind — e.g. (?<=cat|dog) is valid because
        #    both branches are 3 chars wide).
        lengths = {node.fixed_length() for node in self.nodes}

        if len(lengths) == 1 and None not in lengths:
            return lengths.pop()

        return None


_DESIGN_NOTES = """
# Alternation — Logical OR Container

## Relationship to AnyOf
Same self-flattening shape as `Sequence`/`AllOf`, applied to `|` instead
of `+`/`&`. `type(node) is Alternation` exact-type check for the same
reason as elsewhere in this library — a deliberate subclass is never
silently unwrapped.

## Why flattened branches never need wrapping against each other
Once flattened, no branch of an `Alternation` is itself an `Alternation`
— so `node.render(self._precedence)` on a branch that happens to be a
`Sequence` correctly renders UNWRAPPED (SEQUENCE > ALTERNATION means no
wrap), which is exactly right: `cat|dog` doesn't need `(?:cat)|(?:dog)`,
concatenation already binds tighter than alternation with no ambiguity.

## `fixed_length` — the one case genuinely different from Sequence
This is the concrete case flagged in `Regex.fixed_length`'s own
docstring: Python's `re` accepts a lookbehind whose inner pattern is an
alternation of same-length branches (`(?<=cat|dog)`), even though the
branches are different literal text. Using a `set` of the branches'
lengths is a direct, minimal way to check "are they all equal, and none
of them unknown" — `len(lengths) == 1` is only reachable when every
element inserted was the same non-`None` value, since a single `None` in
the set would need `len(lengths) >= 1` too but combined with the
explicit `None not in lengths` check, an all-`None`-but-uniform case
(everything `None`) is correctly rejected as unknown, not miscounted as
"fixed length None".
"""
