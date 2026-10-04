# Outers
from ..base_class import Regex, Precedence
# Inners
from ._helpers import flatten_nodes
from ._validations import raise_no_nodes_error


class Sequence(Regex):
    """Concatenation of regex nodes: node1 followed by node2 followed by ...

    Pattern:
        AB...

    Example:
        Sequence(Literal("ab"), DIGIT)      # -> "ab\\d"
        Literal("ab") + DIGIT               # same, via operator sugar
    """

    __slots__ = ("nodes",)

    _precedence = Precedence.SEQUENCE

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        *nodes: Regex
    ) -> None:

        # 1. Parameter validation
        if not nodes:
            raise_no_nodes_error("Sequence")

        # 2. Flatten nested Sequence instances
        flattened = flatten_nodes(nodes, Sequence, "Sequence")

        # 3. Parameter assignment
        self.nodes: tuple[Regex, ...] = tuple(flattened)

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Render every child against THIS node's own precedence, then
        #    concatenate — each child decides for itself (via `render`)
        #    whether it needs wrapping in this context.
        return "".join(node.render(self._precedence) for node in self.nodes)

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. A sequence has a fixed length only if EVERY child does —
        #    sum them, or bail to None the moment any child is variable.
        total = 0
        for node in self.nodes:
            length = node.fixed_length()
            if length is None:
                return None
            total += length
        return total


_DESIGN_NOTES = """
# Sequence — Concatenation Container

## Relationship to AllOf
Structurally identical constructor shape to `AllOf`: fail-fast on empty
input, self-flattening via exact `type(node) is Sequence` check (not
`isinstance`, for the same reason `AllOf` uses exact type — a deliberate
`Sequence` subclass overriding behavior is never silently unwrapped).

## `to_pattern` delegates wrapping entirely to `render`
`to_pattern` never decides on its own whether a child needs `(?:...)` —
it always calls `node.render(self._precedence)`, and `Regex.render`
(the single, shared implementation) makes that call. 

## `fixed_length` — straightforward sum, strict on unknowns
Unlike `AllOf.is_valid` (which can short-circuit on the first failure),
`fixed_length` cannot short-circuit on the first `None` in a way that
skips work — every child's length is needed to compute the total, so
the loop must inspect them all in order, but it CAN return early the
moment a single `None` appears, since no total is ever reconstructable
after that. This matters only for `Lookaround(direction=BEHIND)`
containing a `Sequence` — the common, expected case.
"""
