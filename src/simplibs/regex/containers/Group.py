# Outers
from ..base_class import Regex, _Precedence
from ..flags.Flag import Flag
# Inners
from ._validations import (
    raise_group_inner_not_regex_error,
    raise_invalid_group_name_error,
    raise_group_atomic_and_name_conflict_error,
    raise_group_atomic_and_flags_conflict_error,
    raise_group_name_and_flags_conflict_error,
    raise_group_name_requires_capturing_error,
    raise_group_flags_require_non_capturing_error,
    raise_group_flags_off_without_flags_error,
)


class Group(Regex):
    """A parenthesized group around `inner`.

    Unifies all 5 Python `re` group syntaxes — capturing, non-capturing,
    named, atomic, and scoped-flags — into one parameterized mechanism
    (Point 2).

    Pattern:
        (A)             capturing=True (default)
        (?:A)           capturing=False
        (?P<name>A)     name="..."
        (?>A)           atomic=True
        (?flags:A)      flags={...}, capturing=False
        (?flags-off:A)  flags={...}, flags_off={...}, capturing=False

    Example:
        Group(DIGIT)                                  # -> "(\\d)"
        Group(DIGIT, capturing=False)                  # -> "(?:\\d)"
        Group(DIGIT, name="year")                       # -> "(?P<year>\\d)"
        Group(DIGIT, atomic=True)                        # -> "(?>\\d)"
        Group(DIGIT, flags={Flag.IGNORECASE})             # -> "(?i:\\d)"
    """

    __slots__ = ("inner", "capturing", "name", "atomic", "flags", "flags_off")

    # A Group is always self-delimiting — its own parentheses ARE the
    # wrap. No child of it ever needs an extra precedence wrap either,
    # since it always renders its inner node at the loosest precedence
    # (see to_pattern).

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        inner: Regex,
        *,
        capturing: bool = True,
        name: str | None = None,
        atomic: bool = False,
        flags: frozenset[Flag] | None = None,
        flags_off: frozenset[Flag] | None = None,
    ) -> None:

        # 1. Parameter validation — inner
        if not isinstance(inner, Regex):
            raise_group_inner_not_regex_error(inner)

        # 2. Parameter validation — name, if given
        if name is not None and not (isinstance(name, str) and name.isidentifier()):
            raise_invalid_group_name_error(name)

        # 3. Parameter validation — mutually exclusive combinations.
        has_flags = bool(flags) or bool(flags_off)

        if atomic and name is not None:
            raise_group_atomic_and_name_conflict_error()
        if atomic and has_flags:
            raise_group_atomic_and_flags_conflict_error()
        if name is not None and has_flags:
            raise_group_name_and_flags_conflict_error()
        if name is not None and not capturing:
            raise_group_name_requires_capturing_error()
        if has_flags and capturing:
            raise_group_flags_require_non_capturing_error()
        if flags_off and not flags:
            raise_group_flags_off_without_flags_error()

        # 4. Parameter assignment
        self.inner = inner
        self.capturing = capturing
        self.name = name
        self.atomic = atomic
        self.flags = flags or frozenset()
        self.flags_off = flags_off or frozenset()

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. The group's own parentheses already delimit `inner`
        #    completely — render it at the loosest possible precedence
        #    (ALTERNATION) so `render` never adds a redundant extra wrap
        #    on top of the one this Group already provides.
        inner_pattern = self.inner.render(_Precedence.ALTERNATION)

        # 2. Build the opening syntax for this specific group variant.
        opening = self._build_opening()

        return f"{opening}{inner_pattern})"

    def _build_opening(self) -> str:
        """Return everything up to and including the opening syntax
        (e.g. "(?P<name>", "(?:", "(?i-m:", "(") for this group variant."""

        # 1. Atomic group.
        if self.atomic:
            return "(?>"

        # 2. Named (always capturing).
        if self.name is not None:
            return f"(?P<{self.name}>"

        # 3. Scoped flags (always non-capturing).
        if self.flags or self.flags_off:
            on_letters = "".join(sorted(f.value for f in self.flags))
            off_letters = "".join(sorted(f.value for f in self.flags_off))
            suffix = f"-{off_letters}" if off_letters else ""
            return f"(?{on_letters}{suffix}:"

        # 4. Plain non-capturing.
        if not self.capturing:
            return "(?:"

        # 5. Plain capturing (the default).
        return "("

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. A group is transparent to match length — it adds capturing
        #    or scoped-flag behavior, never changes how many characters
        #    the inner node consumes.
        return self.inner.fixed_length()


_DESIGN_NOTES = """
# Group — Unified Group Mechanism (Point 2)

## The 5-to-1 collapse
`(A)`, `(?:A)`, `(?P<name>A)`, `(?>A)`, `(?flags:A)`, `(?flags-off:A)`
are one mechanism: an inner node plus a small set of mutually exclusive
modifiers. `_build_opening` picks the right prefix from those
modifiers rather than dispatching to five different classes.

## Why the conflicts are validated explicitly, one at a time
Python's `re` syntax simply has no way to combine `name` with `atomic`,
or either with scoped `flags` — trying to construct such a combination
is a programmer error, not a runtime regex failure, so it is caught at
`Group.__init__` time with a specific, named reason (mirroring
`AllOf`'s `raise_requires_at_least_one_rule_error` — fail fast, with a
message that says exactly which two parameters conflicted, not a
generic "invalid arguments").

## Why `flags_off` alone (without `flags`) is rejected
`(?-imsx:...)` IS valid `re` syntax on its own — but accepting
`Group(x, flags_off={Flag.MULTILINE})` with no `flags` at all invites a
reader to wonder "wait, what flags were even on before this turned one
off" at the call site, since `Group` has no access to any OUTER scope's
active flags to explain it. Requiring `flags` to be passed explicitly
(even as `frozenset()`) keeps every `Group` call site self-explanatory
without needing to trace enclosing scope.

## Why `to_pattern` always renders `inner` at ALTERNATION precedence
Every other container (`Sequence`, `Repeat`) renders children against
ITS OWN `_precedence`, because it has no delimiters of its own and
genuinely needs the precedence comparison to decide whether to wrap.
`Group` is different: its own parentheses are already the delimiter, so
whatever is inside them can never leak out and change meaning —
rendering at ALTERNATION (the loosest level) guarantees `render` never
adds a second, redundant `(?:...)` around something that is already
safely inside `Group`'s own parens. This is the same principle
`Lookaround` and `CharacterClass` will both reuse once written — any
node that provides its own hard delimiters renders children at the
loosest precedence, not at its own.

## `fixed_length` is pure delegation
Matches `IsTyping.build_exception`'s delegation pattern: a `Group`
changes nothing about how many characters get consumed (capturing and
scoped flags are both orthogonal to match width), so re-deriving a
length here would just duplicate `inner.fixed_length()` for no reason.
"""
