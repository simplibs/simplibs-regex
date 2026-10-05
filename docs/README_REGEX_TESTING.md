# 🧪 `regex/testing` — Test Helper for Pattern Terms

The `testing` package holds a single function, `assert_pattern`, a test helper for
anything that is a `Regex` node: the presets in this library, and the vocabulary terms
of libraries built on top of it such as `simplibs-patterns`. It is not part of the DSL
itself and is **not** imported by `simplibs.regex`; import it explicitly.

```python
from simplibs.regex.testing import assert_pattern
```

One call verifies three things about a term: the exact pattern string it renders, the
texts it must match, and the texts it must not match. Terms that only make sense next to
other text (lookarounds) can also be checked in context with `finds`.

```python
def test_digit(subtests):
    assert_pattern(subtests, DIGIT, "\\d", matches=["5"], non_matches=["a", "55"])
```

---

## 🧭 Table of Contents

* [`assert_pattern`](#assert_pattern)
* [Context checks (`finds`)](#context-checks-finds)
* [Verbose and fast mode](#verbose-and-fast-mode)
* [What it does not check](#what-it-does-not-check)

[⬅️ Back to main README](../README.md#testing--test-helper-for-pattern-terms)

---

### `assert_pattern`

Asserts that a `Regex` node renders the expected pattern string and fully matches (or
does not match) the given texts.

**Parameters:**
* `subtests` (*Any*): The `subtests` fixture (provided by `pytest-subtests`). May be
  `None` when `verbose=False`.
* `pattern_obj` (*Regex*): The node under test (e.g. `DIGIT`, or any composed tree).
* `expected_pattern` (*str*): The exact string expected from `pattern_obj.to_pattern()`.
* `matches` (*Sequence[str] | None*, keyword-only, default `None`): Texts that must fully
  match.
* `non_matches` (*Sequence[str] | None*, keyword-only, default `None`): Texts that must
  NOT fully match.
* `finds` (*Mapping[str, str | None] | None*, keyword-only, default `None`): Maps a text to the
  substring a *search* in it must return, or to `None` when nothing may be found — see
  [Context checks](#context-checks-finds).
* `flags` (*set[Flag] | frozenset[Flag]*, keyword-only, default `frozenset()`): Top-level flags
  used when compiling, exactly as in `RegexPattern`.
* `verbose` (*bool*, keyword-only, default `True`): Each check becomes its own subtest
  (`True`), or the first failed check raises immediately (`False`).
* `intro` (*str*, keyword-only, default `""`): Replaces the default subtest-name prefix
  `[expected_pattern]`.

**Returns:**
* `None`

**Raises:**
* `TypeError`: If `pattern_obj` is not a `Regex`, or if `matches` / `non_matches` is a
  bare `str` (it would be iterated character by character), or if `finds` is not a mapping.
* `AssertionError`: If the rendered pattern differs from `expected_pattern`, a text in
  `matches` does not fully match, a text in `non_matches` does, or a `finds` search returns
  something else.

**Example usage:**

```python
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.character_types import DIGIT, WORD_CHARACTER
from simplibs.regex.testing import assert_pattern

# A single term
assert_pattern(subtests, DIGIT, "\\d", matches=["5"], non_matches=["a", "55"])

# With flags
assert_pattern(
    subtests, Literal("abc"), "abc",
    matches=["ABC"],
    flags=frozenset({Flag.IGNORECASE}),
)

# A whole catalog
import pytest


@pytest.mark.parametrize(
    ("node", "expected", "matches", "non_matches"),
    [
        (DIGIT, "\\d", ["5"], ["a", "55"]),
        (WORD, "\\w", ["a", "_"], [" ", "-"]),
    ],
)
def test_presets(subtests, node, expected, matches, non_matches):
    assert_pattern(subtests, node, expected, matches=matches, non_matches=non_matches)
```

**Under the hood:**
```python
actual_pattern = pattern_obj.to_pattern()
with maybe_subtest(subtests, name=f"{prefix}Pattern String Check", verbose=verbose):
    assert actual_pattern == expected_pattern

compiled = RegexPattern(pattern_obj, flags=flags)

for value in matches or ():
    with maybe_subtest(subtests, name=f"{prefix}Match Check ({value!r})", verbose=verbose):
        assert compiled.fullmatch(value) is not None
```

The pattern is compiled through `RegexPattern`, the same path users take, so flags and
construction-time validation behave exactly as in real use. A pattern that cannot
compile at all is a defect of the term itself, so that error is raised once, outside any
subtest, instead of being repeated for every text.

[▲ Back to top](#-table-of-contents)

---

### Verbose and fast mode

* **`verbose=True`** (default): every check is a named subtest, e.g.
  `[\d] Match Check ('5')`. A failure is recorded and the remaining checks still run, so
  one report shows everything wrong with a term. Values are shown with `repr`, so
  whitespace and newlines stay visible.
* **`verbose=False`**: no subtests are created (`subtests` may be `None`) and the first
  failed check raises `AssertionError` immediately — the fast path for large catalogs.

[▲ Back to top](#-table-of-contents)

---

### Context checks (`finds`)

`fullmatch` asks "is this whole text an instance of the term?" — the wrong question for a
lookbehind or lookahead: `(?<=key=).+` can never fully match `"value"`, because nothing
precedes it. `finds` asks the right one: *what does a search in this longer text return?*

```python
assert_pattern(
    subtests, LOOKBEHIND(Literal("USD")) + ONE_OR_MORE(DIGIT), "(?<=USD)\\d+",
    finds={"USD42": "42", "EUR42": None},
)
```

* The key is the text to search, the value the substring the search must return (the whole
  match, `group()`).
* `None` means "nothing may be found".
* Capture groups are not compared; test those directly through `RegexPattern`.

[▲ Back to top](#-table-of-contents)

---

### What it does not check

* **Whole texts only.** Matching uses `fullmatch`, so `matches=["2026-09-30"]` passes
  while `"x2026-09-30x"` belongs in `non_matches`.
* **Zero-width terms.** Anchors and lookarounds consume no characters, so they cannot be
  meaningfully tested with non-empty texts; check them in context with `finds`
  (see above), and rely on the pattern-string check for the rest.
* **Shape, not truth.** The helper checks what a regex can check — see the notes in
  each term's docstring for what a pattern deliberately leaves out (check digits,
  calendar validity, ...).

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#testing--test-helper-for-pattern-terms)