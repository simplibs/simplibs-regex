# 🧵 `RegexPattern` — Compiled Runtime Wrapper

`RegexPattern` is the terminal step of the DSL — build a tree with `Regex` nodes and
operators, then hand the finished tree to `RegexPattern` to actually compile and use
it against real text. A thin, convenient surface over the underlying `re.Pattern`
the tree already knows how to produce; it adds no behavior of its own beyond
compiling once and delegating.

```python
class RegexPattern:
    ...
```

---

## 🧭 Table of Contents

* [`__init__`](#__init__)
* [`pattern_string`](#pattern_string)
* [`search` / `match` / `fullmatch`](#search--match--fullmatch)
* [`findall` / `finditer`](#findall--finditer)
* [`sub` / `subn` / `split`](#sub--subn--split)

[⬅️ Back to main README](../README.md#-regexpattern)

---

### `__init__`

**Parameters:**
* `node` (*Regex*): The root of the composed tree.
* `flags` (*frozenset[Flag]*, keyword-only, default `frozenset()`): Top-level flags —
  see [`README_REGEX_FLAGS`](README_REGEX_FLAGS.md) for the full reference and
  `Flag.LOCALE`'s restriction (rejected here too).
* `description` (*str*, keyword-only, default `""`): Free-text metadata — never
  parsed or inspected internally, carried purely for the caller's benefit
  (self-documenting preset catalogs, readable `repr()` output).
* `lazy` (*bool*, keyword-only, default `False`): If `False` (the default),
  compiles immediately at construction — consistent with every other node's
  fail-fast validation (`Group`, `Lookaround`, `Repeat` all validate in `__init__`).
  If `True`, compilation is deferred to first use (`compiled`, `pattern_string`, or
  any matching method) — a deliberate opt-out for cases like a large catalog of
  named preset patterns where most entries are never actually used in a given run.

**Example usage:**
```python
year = NAMED_GROUP(ONE_OR_MORE(DIGIT), "year")
pattern = RegexPattern(year, flags=frozenset({Flag.IGNORECASE}), description="Four-digit year")

# A preset catalog where most entries go unused — avoid compiling all of them:
EMAIL = RegexPattern(email_node, lazy=True)
```

**Raises:**
* `simplibs.exception.ValidationError` (`REGEX_INVALID_PATTERN_ERROR`): If the fully
  rendered pattern string fails to compile — the one failure no single node's own
  construction-time validation can catch in isolation, most commonly two
  `Group(name=...)` nodes sharing a name at different points in the same tree.
  Raised at construction time when `lazy=False` (the default), or on first use when
  `lazy=True`.

**Under the hood** *(shared by eager and lazy paths via `_ensure_compiled`)*:
```python
def _ensure_compiled(self) -> None:
    if self._compiled is not None:
        return
    pattern_string = self.node.to_pattern()
    combined_flags = 0
    for flag in self.flags:
        combined_flags |= flag.re_flag
    try:
        self._compiled = re.compile(pattern_string, combined_flags)
    except re.error as err:
        raise_invalid_pattern_error(self.node, pattern_string, err)
    self._pattern_string = pattern_string
```

`node.to_pattern()` is walked and `re.compile`d exactly once — mirroring `IsTyping`'s
own reasoning for building its composed rule once in `__init__` rather than on every
evaluation. Reusing the same `RegexPattern` instance across many `search`/`match`
calls never re-walks the tree, and calling `_ensure_compiled` again after the first
successful compilation is always a cheap no-op.

[▲ Back to top](#-table-of-contents)

---

### `pattern_string`

**Property.** The compiled pattern's raw source string, for inspection/debugging.

**Example usage:**
```python
pattern.pattern_string   # -> "(?i:(?P<year>\d+))"
```

[▲ Back to top](#-table-of-contents)

---

### `search` / `match` / `fullmatch`

Thin delegation to the identically-named method on the underlying `re.Pattern`.

**Parameters (each):**
* `text` (*str*): The text to search.
* `pos` (*int*, default `0`): Start position.
* `endpos` (*int | None*, default `None`): End position, if bounding the search.

**Returns:**
* `re.Match | None`

**Example usage:**
```python
m = pattern.search("Born in 2026")
m.group("year")   # -> "2026"
```

[▲ Back to top](#-table-of-contents)

---

### `findall` / `finditer`

**Parameters:**
* `text` (*str*): The text to search.

**Returns:**
* `findall` → `list[Any]`; `finditer` → `Iterator[re.Match]`.

**Example usage:**
```python
pattern.findall("born:1999 born:2000")   # -> ["1999", "2000"]
```

[▲ Back to top](#-table-of-contents)

---

### `sub` / `subn` / `split`

**Parameters:**
* `repl` (*str*): Replacement text (for `sub`/`subn`).
* `text` (*str*): The text to operate on.
* `count` (*int*, default `0`): Max replacements/splits — `0` means unlimited.

**Returns:**
* `sub` → `str`; `subn` → `tuple[str, int]`; `split` → `list[Any]`.

**Example usage:**
```python
pattern.sub("[REDACTED]", "born: 2026")   # -> "[REDACTED]"
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-regexpattern)