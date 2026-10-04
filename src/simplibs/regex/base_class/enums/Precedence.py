from enum import IntEnum


class Precedence(IntEnum):
    """Binding-power levels used by `Regex.render()` to decide whether a
    child node must be wrapped in a non-capturing group before being
    embedded inside a parent node.

    Ordering matches regex operator precedence, from loosest-binding to
    tightest-binding. A child is wrapped whenever its own precedence is
    STRICTLY LOWER than the precedence the parent renders it at — e.g. an
    `Alternation` (ALTERNATION) embedded inside a `Sequence` (SEQUENCE)
    gets wrapped, because ALTERNATION < SEQUENCE.

    ATOM is intentionally the ceiling: anything already self-delimiting
    (a single character, a `Group`, a `CharacterClass`, a `Lookaround`)
    never needs an extra wrap, regardless of where it is embedded.
    """

    ALTERNATION = 0   # A|B  — loosest: spreads across the entire pattern if unwrapped
    SEQUENCE = 1      # AB   — concatenation
    REPEAT = 2        # A*, A{m,n}, ...  — binds to exactly one preceding unit
    ATOM = 3          # single char, Group(...), CharacterClass, Lookaround, Anchor, ...


_DESIGN_NOTES = """
# Precedence — Operator Binding Power

## Purpose
Defines binding-power levels for `Regex.render()` to determine when a child 
node requires wrapping in a non-capturing group.

## Precedence Hierarchy (Loosest to Tightest)
1. `ALTERNATION = 0` (`A|B`) — loosest binding.
2. `SEQUENCE = 1` (`AB`) — concatenation.
3. `REPEAT = 2` (`A*`, `A{m,n}`) — binds to one preceding unit.
4. `ATOM = 3` — ceiling (self-delimiting nodes like groups, character classes, 
anchors, never need wrapping).

## Wrapping Rule
A child is wrapped if its precedence is strictly lower than the parent's 
rendering context (`child_precedence < parent_precedence`).
"""