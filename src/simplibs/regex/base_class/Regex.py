import re
from abc import ABC, abstractmethod
# Inners
from .enums import Precedence


class Regex(ABC):
    """Abstract base class for every node of the regex DSL.

    Every concrete node (container or atom) inherits from this class and
    implements `to_pattern` and, where a fixed length is knowable,
    `fixed_length`. The class provides precedence-aware rendering via
    `render`, fixed-length introspection for lookbehind validation, a
    character-class-item opt-in marker, and the `+` (Sequence) and `|`
    (Alternation) composition operators.
    """

    # ----------------------------------------------------------------------
    # Class-level contract every subclass declares
    # ----------------------------------------------------------------------

    # Binding power of THIS node's own top-level syntax, used by
    # a parent's `render()` to decide whether this node needs wrapping.
    # Defaults to ATOM (self-delimiting) — Sequence, Alternation and Repeat
    # explicitly override this to a lower value.
    _precedence: Precedence = Precedence.ATOM

    # True on nodes that are legal standalone
    # items inside a CharacterClass (`[...]`), where escape semantics
    # differ from the rest of the pattern (see CharacterClass's own
    # validation, which checks this flag rather than a broad isinstance
    # check against the whole Regex hierarchy). Defaults to False; only
    # CharacterType, CharacterRange, CharacterCode and single-character
    # Literal override it to True.
    _usable_in_char_class: bool = False

    # False on nodes that `re` refuses to quantify directly: a quantifier
    # placed straight after them fails with "nothing to repeat" (`^*`,
    # `\b?`). `Repeat` reads this flag in its constructor and rejects such a
    # node up front, instead of letting the error surface later in
    # `re.compile()`. Defaults to True; only Anchor overrides it to False.
    # The flag describes the BARE node: an anchor wrapped in a Group, or a
    # Lookaround, is accepted by `re` and therefore stays True.
    _repeatable: bool = True

    # ----------------------------------------------------------------------
    # 1) Abstract Interface (mandatory for subclasses)
    # ----------------------------------------------------------------------

    @abstractmethod
    def to_pattern(self) -> str:
        """Return this node's own regex fragment, WITHOUT any wrapping
        that depends on where it is embedded.

        Containers call `child.render(self._precedence)` on their
        children instead of `child.to_pattern()` directly, so that
        wrapping decisions are made once, in one place (`render`), never
        duplicated per-container. Implementations of `to_pattern` should
        therefore never wrap their own output in `(?:...)` for precedence
        reasons — only for syntax that is mandatory regardless of context
        (e.g. `Group` always emits its own parentheses; that is not a
        precedence wrap, it is the node's literal syntax).
        """
        raise NotImplementedError

    # ----------------------------------------------------------------------
    # 2) Fixed-Length Introspection
    # ----------------------------------------------------------------------

    def fixed_length(self) -> int | None:
        """Return this node's match length in characters if — and only
        if — it is fixed regardless of input, otherwise `None`.

        Used by `Lookaround` (direction=BEHIND) to fail fast at
        construction time when Python's `re` would otherwise reject a
        variable-length lookbehind, instead of surfacing that failure
        only later at `re.compile()`.

        Default: `None` (unknown / variable). A node that CAN determine
        a fixed length overrides this:
        * `Literal` -> `len(text)`
        * `CharacterType` / `CharacterClass` -> 1; `Anchor` / `Lookaround`
          (zero-width) -> 0
        * `Sequence` -> sum of children's fixed lengths, or `None` if any
          child is `None`
        * `Repeat` -> `min * inner_length` when `min == max` and inner has
          a fixed length, else `None`
        * `Alternation` -> the shared length if every branch has the SAME
          fixed length, else `None` (Python's `re` does support
          same-length alternation inside a lookbehind)

        Never guess: returning a wrong non-`None` value here would let an
        invalid lookbehind slip past construction-time validation only to
        fail confusingly later, or (worse) silently compile something
        other than what the user intended.
        """
        return None

    def needs_wrap_for_repeat(self) -> bool:
        """Return True if this node, despite rendering at ATOM precedence
        (no wrap from `render`'s ordinary precedence comparison), still
        needs an explicit `(?:...)` wrap before a `Repeat` quantifier can
        be applied to it as a single unit.

        Exists for exactly one case in the whole hierarchy: a
        multi-character `Literal`. Quantifiers in `re` bind to the single
        preceding token — a character, an escape sequence, a character
        class, or a group — never to more than one character of plain
        text. `Literal`'s own `_precedence` correctly stays at ATOM (it
        needs no wrap when embedded in a `Sequence` or `Alternation`),
        so `_precedence` alone cannot express this narrower,
        repeat-specific constraint; this separate hook does.

        Default: `False` — every other ATOM-precedence node (`Anchor`,
        `CharacterType`, `CharacterClass`, `Group`, `Lookaround`,
        `GroupReference`, `CharacterCode`) is already exactly one token by
        construction and never needs this.
        """
        return False

    def to_char_class_fragment(self) -> str:
        """Return this node's representation for use as a standalone item
        inside a `CharacterClass` (`[...]`), where escaping rules differ
        from the rest of a pattern.

        Default: identical to `to_pattern()` — correct for every node
        whose escape syntax is genuinely the same inside and outside a
        character class (`CharacterType`, `CharacterCode`). Only `Literal`
        overrides this, since a character class only ever needs to
        escape `] ^ - \\`, a different and much smaller set than the
        general-purpose `re.escape` used by `Literal.to_pattern`.

        Only ever called on nodes where `_usable_in_char_class` is
        `True` — `CharacterClass.__init__` is responsible for that
        check; this method itself does not re-validate it.
        """
        return self.to_pattern()

    # ----------------------------------------------------------------------
    # 3) Precedence-Aware Rendering
    # ----------------------------------------------------------------------

    def render(self, parent_precedence: "Precedence") -> str:
        """Render this node for embedding inside a parent whose own
        binding power is `parent_precedence`.

        Wraps `to_pattern()`'s output in a non-capturing group exactly
        when this node's own `_precedence` is strictly lower than the
        parent's — e.g. an `Alternation` embedded inside a `Sequence`
        gets wrapped, because ALTERNATION < SEQUENCE. A node whose
        precedence is ATOM (the default) is never wrapped, since it is
        already self-delimiting.

        This is the ONLY place precedence wrapping happens. Containers
        (`Sequence`, `Repeat`, ...) must call `child.render(self._precedence)`
        on every child instead of `child.to_pattern()` directly.
        """
        fragment = self.to_pattern()

        if self._precedence < parent_precedence:
            return f"(?:{fragment})"

        return fragment

    # ----------------------------------------------------------------------
    # 4) Public Interface
    # ----------------------------------------------------------------------

    def compile(self, flags: int = 0) -> re.Pattern[str]:
        """Compile this node's top-level pattern via `re.compile`.

        Top-level rendering always uses `to_pattern()` directly (never
        `render()`) — there is no parent context to wrap against at the
        root of the tree.
        """
        return re.compile(self.to_pattern(), flags)

    # ----------------------------------------------------------------------
    # 5) Operator-Based Composition (+, |)
    # ----------------------------------------------------------------------
    #
    # `+` builds Sequence, `|` builds Alternation — deliberately different
    # operators from Rule's `&`/`|`, since regex composition has no
    # boolean AND: two nodes next to each other in a pattern concatenate,
    # they do not both have to "pass". `|` is the one operator that keeps
    # its meaning from Rule/Action, since regex alternation IS a direct
    # analogue of logical OR.

    def __add__(self, other: "Regex") -> "Regex":
        """Concatenate with another node via `node1 + node2`.

        Equivalent to `Sequence(self, other)`. Returns `NotImplemented`
        for anything that is not a `Regex` instance, letting Python fall
        back to `other.__radd__(self)` or raise `TypeError` as usual.
        """
        if isinstance(other, Regex):
            from ..containers.Sequence import Sequence

            return Sequence(self, other)
        return NotImplemented

    def __radd__(self, other: "Regex") -> "Regex":
        """Support `other + node` when `other` has no (or a declining) `__add__`."""
        if isinstance(other, Regex):
            from ..containers.Sequence import Sequence

            return Sequence(other, self)
        return NotImplemented

    def __or__(self, other: "Regex") -> "Regex":
        """Combine with another node via alternation: `node1 | node2`.

        Equivalent to `Alternation(self, other)`.
        """
        if isinstance(other, Regex):
            from ..containers.Alternation import Alternation

            return Alternation(self, other)
        return NotImplemented

    def __ror__(self, other: "Regex") -> "Regex":
        """Support `other | node` when `other` has no (or a declining) `__or__`."""
        if isinstance(other, Regex):
            from ..containers.Alternation import Alternation

            return Alternation(other, self)
        return NotImplemented

    def __repr__(self) -> str:
        """Return a concise unambiguous representation of the Regex node."""
        return f"{self.__class__.__name__}({self.to_pattern()!r})"

_DESIGN_NOTES = """
# Regex — Base Abstract Class for the Regex DSL

## Relationship to Rule / Action
Same three-part shape: (1) an abstract production method every subclass
must implement (`to_pattern`, mirroring `is_valid`/`__call__`), (2) a
public convenience surface (`render`, `compile`), (3) operator-based
composition delegating to lazily-imported containers, exactly like
`Rule.__and__`/`Action.__and__` deferring to `AllOf`/`ParallelCompose`.

The one new piece with no Rule/Action equivalent is `fixed_length` —
regex composition has no analogue to "does this predicate pass", but it
does have "how wide is this fragment", and that question only exists
because `Lookaround(direction=BEHIND)` needs an answer to it at
construction time.

## Why `render()` lives on the base class, not repeated per container
Every container (`Sequence`, `Alternation`, `Repeat`, `Group`, ...) needs
the exact same decision procedure for wrapping a child: compare
precedences, wrap or don't. Putting that once on `Regex.render()` and
having containers call `child.render(self._precedence)` means the
wrapping RULE has exactly one implementation in the whole library — a
container never decides FOR ITSELF whether to wrap a child, it just
states its own precedence and asks the child to render into that
context. This mirrors how `AllOf.build_exception` doesn't reimplement
diagnostic formatting — it delegates to `build_child_exception`.

## Why `_precedence` defaults to ATOM rather than being abstract
Most nodes in the tree (`Literal`, `CharacterType`, `Anchor`,
`GroupReference`, `CharacterCode`, and every container that already emits its
own delimiters — `Group`, `CharacterClass`, `Lookaround`, `Conditional`)
are self-delimiting and never need wrapping. Only `Sequence`,
`Alternation`, and `Repeat` have a real precedence below ATOM and must
override the class attribute. Making ATOM the default means the large,
common case (leaf nodes) declares nothing extra — only the few
containers where it actually matters opt out of the default.

## Why `fixed_length` is a concrete method with a safe default, not abstract
Unlike `to_pattern` (every node MUST be renderable) or `is_valid` on
`Rule` (every rule MUST be evaluable), most nodes genuinely don't need an
exact answer to "how long am I" — only `Lookaround` ever asks the
question. Defaulting to `None` ("unknown/variable") is always SAFE: a
node that fails to override this when it actually has a fixed length
only loses the ability to be used inside a lookbehind directly (it can
still always be wrapped in an explicit, hand-verified way) — it can
never cause a wrong pattern to compile, because `None` is
construction-time-rejected by `Lookaround`, never silently accepted.

## `_usable_in_char_class` is a flag, not a separate hierarchy
Chosen deliberately over fully separate `CharacterClassItem`/`Atom` class
hierarchies (the alternative discussed as "variant 1" in the design
review): a single `Regex` hierarchy stays consistent with `Rule`'s own
single-hierarchy shape, and `CharacterClass.__init__` enforces the
restriction procedurally — via `isinstance(item, Regex) and
item._usable_in_char_class` — the same procedural-check pattern
`Rule.__and__` already uses for `__not_rule__`. This is intentionally
closer to variant 2 of the original write-up (runtime marker, not a
type-level split) — full static separation would require either
duplicating `CharacterType`/`CharacterCode` under two class hierarchies or
introducing a shared mixin/Protocol layer whose benefit (catching a
`CharacterClass(WordBoundary())` mistake at type-check time instead of
at construction time) did not outweigh the added structural complexity
for this first pass. `CharacterClass`'s own design notes will document
this decision again alongside its actual constructor.

## `compile()` uses `to_pattern()` directly, never `render()`
There is no parent node at the root of a tree, so there is no
`parent_precedence` to render against. Calling `render()` at the root
would require inventing a fake top-level precedence — `to_pattern()` is
the honest choice: the root always emits its own fragment unwrapped.

## `needs_wrap_for_repeat` — a narrower hook than `_precedence`.
`Repeat` needs to know something `_precedence` genuinely cannot express:
not "does this need parentheses to avoid changing meaning in a larger
expression" (that's precedence), but "is this exactly one quantifiable
token". Those two questions have the same answer for every ATOM node
except a multi-character `Literal`, which is why this is a separate
method with a safe default (`False`) rather than a new `Precedence`
level — inventing a level for a single-class exception would have
forced every other atom to reason about a distinction that, for them,
never varies.

## `_repeatable` — "may a quantifier follow me at all?"
`needs_wrap_for_repeat` answers "does `Repeat` have to add parentheses
around me?"; `_repeatable` asks the question before it: can a quantifier
be applied to me in any form? For almost every node the answer is yes
(sometimes after a wrap), so the default is `True`. The exception is the
bare anchors `^ $ \\A \\Z \\b \\B`: there is nothing for the quantifier to
bind to, and `re` fails with "nothing to repeat" (verified against
`re.compile`: `^*`, `\\b?`, `\\A?`, `a\\Z*`).

Zero-width does NOT mean unrepeatable. `(?=a)*` and `(\\b)*` compile, so
lookarounds and a group around an anchor stay `True`; the flag is a
property of the node type, not of "everything with width 0".

Why a flag, and not `isinstance(inner, Anchor)` inside `Repeat`: that
check would make `containers/` import from `elements/`, a dependency
pointing against the layering, and every future node with the same
limitation would require editing `Repeat`. With the flag `Repeat` only
asks the node — the same shape as `CharacterClass` asking
`_usable_in_char_class`.

Why `Repeat` refuses instead of silently wrapping the anchor as
`(?:^)*`: that would compile, but repeating a zero-width assertion
changes nothing, so the author almost certainly meant something else
(an optional position, a lookaround). Failing at the line that built the
node, with a message naming both ways out, is more useful than a pattern
that quietly does less than it looks like.

The four hooks answer four separate questions and are kept separate on
purpose:
* `_precedence` — how must I be wrapped when embedded in a parent?
* `needs_wrap_for_repeat` — must `Repeat` add parentheses around me?
* `_repeatable` — may a quantifier follow me at all?
* `_usable_in_char_class` — may I appear inside `[...]`?

## `to_char_class_fragment` — a narrower rendering hook.
Same shape of decision as `needs_wrap_for_repeat`: the DEFAULT
implementation (delegate straight to `to_pattern`) is correct for the
common case (`CharacterType`, `CharacterCode` — genuinely the same escape
syntax either side of `[...]`), and only the one node where the two
contexts actually diverge (`Literal`) overrides it. Kept as a separate
method rather than a branch inside `to_pattern` itself, because
`to_pattern`'s job is "render me as a normal fragment" — conflating
that with "render me as a character-class item" would make every node
that never appears inside a class carry dead branching for a context
that can never apply to it.

## Why `+` for Sequence instead of reusing `&`
`Rule.__and__` means "both predicates must hold" — a genuine boolean AND.
Two regex nodes placed next to each other don't "both have to hold" in
that sense; they concatenate. Using `&` for that would silently imply a
semantics this DSL does not have (and `&` is already claimed by
`Action` for a different, execution-parallel meaning) — `+` reads
correctly as "these go one after another" and has no prior claimed
meaning in either sibling library.
"""