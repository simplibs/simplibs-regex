import re
from typing import Any, Iterator
# Outers
from ..base_class import Regex
from ..flags.Flag import Flag
# Inners
from ._validations import (
    raise_invalid_pattern_error,
    raise_invalid_locale_error,
    raise_param_invalid_type_error
)


class RegexPattern:
    """Compiled, ready-to-use wrapper around a `Regex` tree.

    The terminal step of the DSL: builds the tree with `Regex` nodes and
    operators, then hands the finished tree to `RegexPattern` to actually
    compile and use it against real text. Mirrors `Rule.validate` in
    spirit — a thin, convenient surface over the underlying `re.Pattern`
    that the tree already knows how to produce.

    Example:
        year = NAMED_GROUP(ONE_OR_MORE(DIGIT), "year")
        pattern = RegexPattern(year, description="A four-digit calendar year")
        match = pattern.search("Born in 2026")
        match.group("year")   # -> "2026"
    """

    __slots__ = ("node", "flags", "description", "lazy", "_pattern_string", "_compiled")

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        node: Regex,
        *,
        flags: set[Flag] | frozenset[Flag] = frozenset(),
        description: str = "",
        lazy: bool = False,
    ) -> None:

        # 1. Parameter validation — types
        if not isinstance(node, Regex):
            raise_param_invalid_type_error("node", node)
        if not isinstance(flags, (set, frozenset)) or not all(isinstance(f, Flag) for f in flags):
            raise_param_invalid_type_error("flags", flags)
        if not isinstance(description, str):
            raise_param_invalid_type_error("description", description)
        if not isinstance(lazy, bool):
            raise_param_invalid_type_error("lazy", lazy)

        # 2. Parameter validation — LOCALE cannot be used with str patterns
        if Flag.LOCALE in flags:
            raise_invalid_locale_error(flags)

        # 3. Parameter assignment
        self.node = node
        self.flags = frozenset(flags)
        self.description = description
        self.lazy = lazy
        self._pattern_string: str | None = None
        self._compiled: re.Pattern[str] | None = None

        # 4. Eager compilation (the default) — fail fast at construction time
        if not self.lazy:
            self._ensure_compiled()

    # ----------------------------------------------------------------------
    # Compilation — shared by eager (__init__) and lazy (first access)
    # ----------------------------------------------------------------------
    def _ensure_compiled(self) -> None:
        """Compile once, on first need, and cache. Safe to call
        repeatedly — a no-op once `self._compiled` is already set."""

        # 1. Already compiled — nothing to do
        if self._compiled is not None:
            return

        # 2. Render the tree to a pattern string
        pattern_string = self.node.to_pattern()

        # 3. Combine requested flags into one integer for re.compile
        combined_flags = 0
        for flag in self.flags:
            combined_flags |= flag.re_flag

        # 4. Compile the pattern, wrapping any compile failure into a structured
        #    diagnostic. `re.compile` raises ValueError (not re.error) for
        #    incompatible flags such as ASCII together with UNICODE.
        try:
            self._compiled = re.compile(pattern_string, combined_flags)
        except (re.error, ValueError) as err:
            raise_invalid_pattern_error(self.node, pattern_string, err)

        # 5. Cache the pattern string
        self._pattern_string = pattern_string

    @property
    def compiled(self) -> re.Pattern[str]:
        """The compiled `re.Pattern` — compiled on first access and
        cached if `lazy=True` was requested; already compiled otherwise."""
        self._ensure_compiled()
        # noinspection PyTypeChecker
        return self._compiled

    # ----------------------------------------------------------------------
    # Public Interface — thin delegation to the underlying re.Pattern
    # ----------------------------------------------------------------------

    @property
    def pattern_string(self) -> str:
        """The compiled pattern's raw source string, for inspection/debugging."""
        self._ensure_compiled()
        # noinspection PyTypeChecker
        return self._pattern_string

    def search(self, text: str, pos: int = 0, endpos: int | None = None) -> "re.Match[str] | None":
        """Scan through string looking for the first location where this pattern produces a match."""
        if endpos is None:
            return self.compiled.search(text, pos)
        return self.compiled.search(text, pos, endpos)

    def match(self, text: str, pos: int = 0, endpos: int | None = None) -> "re.Match[str] | None":
        """If zero or more characters at the beginning of string match this pattern, return a corresponding Match object."""
        if endpos is None:
            return self.compiled.match(text, pos)
        return self.compiled.match(text, pos, endpos)

    def fullmatch(self, text: str, pos: int = 0, endpos: int | None = None) -> "re.Match[str] | None":
        """If the whole string matches this pattern, return a corresponding Match object."""
        if endpos is None:
            return self.compiled.fullmatch(text, pos)
        return self.compiled.fullmatch(text, pos, endpos)

    def findall(self, text: str) -> list[Any]:
        """Return all non-overlapping matches of pattern in string, as a list of strings or tuples."""
        return self.compiled.findall(text)

    def finditer(self, text: str) -> Iterator["re.Match[str]"]:
        """Return an iterator yielding match objects over all non-overlapping matches for the pattern in string."""
        return self.compiled.finditer(text)

    def sub(self, repl: str, text: str, count: int = 0) -> str:
        """Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by replacement."""
        return self.compiled.sub(repl, text, count)

    def subn(self, repl: str, text: str, count: int = 0) -> tuple[str, int]:
        """Return a tuple of (new_string, number_of_subs_made) using the replacement."""
        return self.compiled.subn(repl, text, count)

    def split(self, text: str, maxsplit: int = 0) -> list[Any]:
        """Split string by the occurrences of pattern."""
        return self.compiled.split(text, maxsplit)

    def __repr__(self) -> str:
        """Return a concise unambiguous representation of the RegexPattern instance."""
        desc = f", description={self.description!r}" if self.description else ""
        return f"RegexPattern({self.node!r}, flags={self.flags!r}{desc})"


_DESIGN_NOTES = """
# RegexPattern — Runtime Wrapper

## Relationship to the tree, and to Rule.validate
`RegexPattern` is intentionally the ONLY place `re.compile` is called
against a tree's own `to_pattern()` output during ordinary use
(`Regex.compile()` also calls it, but that is a debugging/introspection
convenience — see `Regex.py`'s own design notes — not the primary
entry point). Every DSL construction happens through `Regex` nodes and
operators; `RegexPattern` is the terminal step, the same way
`Rule.validate` is the terminal step that actually DOES something with
an otherwise inert composed `Rule` tree.

## `description` — free-text, never used internally
Carried purely for the caller's own benefit — self-documenting preset
catalogs (`RegexPattern(year_pattern, description="A four-digit
calendar year")`) and readable `repr()` output. Never parsed, compared,
or otherwise inspected by this class itself; it is pure metadata.

## `lazy` — eager by default, opt-in lazy
Every other node in this library validates fully at construction time —
`Group`, `Lookaround`, and `Repeat` all raise in `__init__`, never on
first use. `RegexPattern` keeps that same fail-fast default: a bad tree
is caught the moment it's wrapped, not the moment it's first searched
against real text, three call sites away from where the mistake was
made.

`lazy=True` is a deliberate, narrow opt-out for the one case where eager
compilation is pure waste: a large catalog of named preset patterns
(module-level `RegexPattern` constants, the shape a `lexicon`-style
vocabulary layer built on top of this library would produce many of),
where any single run only ever touches a handful of them. Compiling
every entry at import time in that scenario is real, avoidable cost
with no corresponding benefit — nothing about WHEN a rarely-used preset
fails is more useful at import time than at first actual use.

Both eager and lazy funnel through the same `_ensure_compiled` — there
is exactly one compilation code path, called either once from
`__init__` or once from the first `compiled`/`pattern_string` access;
`_compiled is not None` makes every subsequent call a cheap no-op
either way.

## Why the invalid-pattern error is wrapped here, not left as bare re.error
Every OTHER construction-time failure in this library — a variable-
length lookbehind, an invalid flag combination, an out-of-range
CharacterCode — is caught by the specific node that owns that constraint,
with a message naming exactly what's wrong. A genuinely cross-tree
conflict (two `Group(name=...)` nodes sharing a name at different
points in the tree) is structurally impossible for any single node to
catch in isolation — nothing has visibility into the WHOLE tree until
`to_pattern()` has already produced one flat string and `re.compile`
parses it as a unit. `raise_invalid_pattern_error` exists so that this
one remaining class of failure still surfaces through the same
structured-diagnostic convention (`simplibs.exception.ValidationError`)
the rest of the ecosystem's `raise_*` helpers already use, rather than
being the one place a bare `re.error` leaks out unexplained.

## Why this is otherwise a thin delegator, not a re-implementation
Every matching/extraction method here does exactly one thing: forward
to the identically-named method on `self.compiled`. No behavior is
added or changed beyond the lazy/eager compilation gate itself —
`RegexPattern` exists purely to be the thing a `Regex` tree naturally
turns into once you're done composing it, not a new abstraction over
`re.Pattern`'s own well-established interface.
"""