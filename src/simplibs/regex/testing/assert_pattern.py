from collections.abc import Sequence
from typing import Any
from simplibs.exception.testing import maybe_subtest
# Outers
from ..base_class import Regex
from ..compiler.RegexPattern import RegexPattern
from ..flags.Flag import Flag


def assert_pattern(
    subtests: Any,
    pattern_obj: Regex,
    expected_pattern: str,
    *,
    matches: Sequence[str] | None = None,
    non_matches: Sequence[str] | None = None,
    flags: set[Flag] | frozenset[Flag] = frozenset(),
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that a Regex node renders the expected pattern and matches the expected texts.

    Verifies the core contract of any pattern term in this library:
    1. Pattern string: `pattern_obj.to_pattern() == expected_pattern`.
    2. Positive matching: every string in `matches` fully matches.
    3. Negative matching: no string in `non_matches` fully matches.

    Args:
        subtests: The pytest-subtests fixture. May be None when `verbose=False`.
        pattern_obj: The Regex node under test (e.g. `DIGIT`, `ISO_DATE`).
        expected_pattern: The exact string expected from `pattern_obj.to_pattern()`.
        matches: Strings that must fully match (list or tuple, not a bare str).
        non_matches: Strings that must NOT fully match (list or tuple, not a bare str).
        flags: Top-level flags used when compiling (e.g. `frozenset({Flag.IGNORECASE})`).
        verbose: If True, each check is an isolated subtest; if False, the first
            failed check raises immediately.
        intro: Optional subtest-name prefix replacing the default `[expected_pattern]`.

    Raises:
        TypeError: If `pattern_obj` is not a Regex or `matches`/`non_matches` is a bare str.
        AssertionError: If the pattern string differs or any match check fails.
    """

    # 1. Parameter validation
    if not isinstance(pattern_obj, Regex):
        raise TypeError(
            f"assert_pattern() requires a Regex instance, got {pattern_obj!r} "
            f"of type '{type(pattern_obj).__name__}'."
        )
    for name, values in (("matches", matches), ("non_matches", non_matches)):
        if isinstance(values, str):
            raise TypeError(
                f"assert_pattern() '{name}' must be a list of strings, not a "
                f"single str ({values!r}) — it would be iterated character by character."
            )

    # 2. Subtest name prefix
    prefix = f"{intro} " if intro else f"[{expected_pattern}] "

    # 3. Pattern string check
    actual_pattern = pattern_obj.to_pattern()
    with maybe_subtest(subtests, name=f"{prefix}Pattern String Check", verbose=verbose):
        assert actual_pattern == expected_pattern, (
            f"Expected pattern string '{expected_pattern}', got '{actual_pattern}'."
        )

    # 4. Compile through the real runtime wrapper (the path users take)
    compiled = RegexPattern(pattern_obj, flags=flags)

    # 5. Positive matching check
    for value in matches or ():
        with maybe_subtest(subtests, name=f"{prefix}Match Check ({value!r})", verbose=verbose):
            assert compiled.fullmatch(value) is not None, (
                f"Expected pattern '{expected_pattern}' to match value {value!r}."
            )

    # 6. Negative matching check
    for value in non_matches or ():
        with maybe_subtest(subtests, name=f"{prefix}Non-Match Check ({value!r})", verbose=verbose):
            assert compiled.fullmatch(value) is None, (
                f"Expected pattern '{expected_pattern}' NOT to match value {value!r}."
            )


_DESIGN_NOTES = """
# assert_pattern (Pattern Contract Verification)

## Purpose
The canonical helper for verifying a single pattern term: a preset in
`simplibs-regex` or a vocabulary term in `simplibs-patterns`. One call
checks three things: the exact rendered pattern string, the texts the
pattern must fully match, and the texts it must not match.

---

## 1. Mechanical check first, behavioural checks second
The string check (`to_pattern() == expected_pattern`) pins down the exact
regex a term produces, so an accidental change in the tree is caught even
when the behaviour happens to stay the same. The `matches` and
`non_matches` lists then prove the pattern does what its docstring
promises. The two kinds of check are independent: a wrong string never
hides a wrong match, and vice versa.

## 2. Why it ships inside the package, not in `tests/`
`simplibs-patterns` tests import this helper from an installed
`simplibs-regex`. It deliberately does not import `pytest`: the
`pytest-subtests` fixture is passed in as the `subtests` argument, so the
helper adds no test-framework dependency to the library.

## 3. Subtests through `maybe_subtest`
* `verbose=True`: every check is its own named subtest. A failure is
  recorded and the remaining checks still run, so one report shows
  everything that is wrong with a term.
* `verbose=False`: no subtest is created (`subtests` may then be `None`)
  and the first failed check raises `AssertionError` immediately, which
  is the fast path for large catalogs.
Routing both lanes through `maybe_subtest` keeps the helper free of
repeated `if verbose` blocks.

## 4. Compiled through `RegexPattern`
The pattern is compiled exactly the way users compile it, with the same
flag handling, so a term that only works with a particular `flags` value
is tested with it. A pattern that cannot compile at all is a defect of
the term, not of one value, so the resulting error is raised outside any
subtest instead of being repeated for every text.

## 5. Why `fullmatch`
`matches` and `non_matches` describe whole texts. `fullmatch` makes
"matches" mean "this entire text is an instance of the term", so
`"2026-09-30"` is accepted and `"x2026-09-30x"` is not. The consequence:
zero-width terms (anchors, lookarounds) cannot be tested with non-empty
texts, so for them the string check is the test.

## 6. Fail-fast guards
* `pattern_obj` must be a `Regex`, otherwise `TypeError`.
* `matches` / `non_matches` must not be a bare `str`. A single string
  would be iterated character by character and produce a test that
  looks valid but checks something else entirely, so it is rejected.

## 7. Subtest names
The default prefix is `[expected_pattern]`, not the class name: every
`CharacterType` preset has the same class name, while the pattern string
tells `DIGIT` and `WORD` apart at a glance. Tested values are shown with
`repr`, so whitespace and newlines stay visible. `intro` replaces the
prefix when a more descriptive name is wanted.
"""