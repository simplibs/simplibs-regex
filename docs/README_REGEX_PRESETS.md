# 🎁 `regex/presets` — Ready-Made Instances & Factories

The `presets` package holds no logic of its own — every entry here is either a
pre-built `Regex` instance (`DIGIT`, `START`) or a small factory function returning
one (`ONE_OR_MORE(inner)`, `NAMED_GROUP(inner, name)`), built directly on top of the
mechanisms in `elements/`/`containers/`/`flags/`. Grouped by module below; each card is
the preset's full behavior, parameters, and example.

```python
DIGIT = CharacterType(CharacterTypeKind.DIGIT)

def ONE_OR_MORE(inner: Regex, *, mode: RepeatMode = RepeatMode.GREEDY) -> Repeat:
    return Repeat(inner, min=1, max=None, mode=mode)
```

## A note on scope

`CharacterClass` and `Group` stay deliberately open, general mechanisms — this
package does not try to anticipate every combination a caller might want. Presets
exist only where a construct is either genuinely fixed (an anchor, a character type)
or common and tedious/error-prone enough to retype correctly by hand (`HEX_DIGIT`,
`CASE_INSENSITIVE`). Anything more specific is expected to be composed directly from
the underlying mechanisms.

---

## 🧭 Table of Contents

[**anchors**: `START` · `END` · `START_STRING` · `END_STRING` ·
`WORD_BOUNDARY` · `NON_WORD_BOUNDARY`](#anchors)

[**any_character**: `ANY`](#any_character)

[**character_types**: `DIGIT` · `NON_DIGIT` · `WORD` · `NON_WORD` ·
`WHITESPACE` · `NON_WHITESPACE`](#character_types)

[**character_classes**: `LOWERCASE_LETTER` ·
`UPPERCASE_LETTER` · `LETTER` · `ALPHANUMERIC` · `HEX_DIGIT`](#character_classes)

[**literals**: `TAB` · `NEWLINE` · `CARRIAGE_RETURN` · `FORM_FEED` ·
`VERTICAL_TAB` · `BELL` · `BACKSLASH_CHAR`](#literals)

[**quantifiers**: `OPTIONAL` · `ZERO_OR_MORE` · `ONE_OR_MORE` ·
`EXACTLY` · `AT_LEAST` · `BETWEEN`](#quantifiers)

[**groups**: `NAMED_GROUP` · `NON_CAPTURING` · `ATOMIC_GROUP` ·
`WITH_FLAGS` · `CASE_INSENSITIVE` · `VERBOSE_GROUP`](#groups)

[**lookaround**: `LOOKAHEAD` · `NEGATIVE_LOOKAHEAD` · `LOOKBEHIND` ·
`NEGATIVE_LOOKBEHIND`](#lookaround)

[⬅️ Back to main README](../README.md#presets--ready-made-instances--factories)

---

### `anchors`

Module-level `Anchor` instances — see
[`README_REGEX_ELEMENTS`](README_REGEX_ELEMENTS.md#anchor) for the full `AnchorKind`
reference.

| Preset | Renders |
|---|---|
| `START` | `^` |
| `END` | `$` |
| `START_STRING` | `\A` |
| `END_STRING` | `\Z` |
| `WORD_BOUNDARY` | `\b` |
| `NON_WORD_BOUNDARY` | `\B` |

`END` (`$`) also matches just before a trailing newline at the end of the string; use
`END_STRING` for the strict end.

> ⚠️ No eager preset for `AnchorKind.END_STRING_PY314` (`\z`) — building one at
> import time would version-check (and crash) on every interpreter below 3.14. Build
> it directly on 3.14+: `Anchor(AnchorKind.END_STRING_PY314)`.

**Example usage:**
```python
Sequence(START_STRING, Literal("ab"), END_STRING)   # -> "\Aab\Z"
```

[▲ Back to top](#-table-of-contents)

---

### `any_character`

A single stateless singleton — see
[`README_REGEX_ELEMENTS`](README_REGEX_ELEMENTS.md#anycharacter).

| Preset | Renders |
|---|---|
| `ANY` | `.` |

**Example usage:**
```python
ANY.to_pattern()   # -> "."
```

[▲ Back to top](#-table-of-contents)

---

### `character_types`

Module-level `CharacterType` instances — see
[`README_REGEX_ELEMENTS`](README_REGEX_ELEMENTS.md#charactertype).
Like `re` itself they are Unicode-aware for `str` patterns (`DIGIT` also matches digits of
other scripts); compile with `Flag.ASCII` to restrict them to ASCII.

| Preset | Renders |
|---|---|
| `DIGIT` | `\d` |
| `NON_DIGIT` | `\D` |
| `WORD` | `\w` |
| `NON_WORD` | `\W` |
| `WHITESPACE` | `\s` |
| `NON_WHITESPACE` | `\S` |

**Example usage:**
```python
CharacterClass(DIGIT, WHITESPACE)   # -> "[\d\s]"
```

[▲ Back to top](#-table-of-contents)

---

### `character_classes`

Common `CharacterClass` compositions — ASCII letter ranges, alphanumeric, and hex
digit. `ALPHANUMERIC`/`HEX_DIGIT` deliberately use ASCII `CharacterRange("0", "9")`
rather than the Unicode-aware `DIGIT` preset, so they stay strictly ASCII as a reader
would expect by convention.

| Preset | Renders |
|---|---|
| `LOWERCASE_LETTER` | `[a-z]` |
| `UPPERCASE_LETTER` | `[A-Z]` |
| `LETTER` | `[a-zA-Z]` |
| `ALPHANUMERIC` | `[a-zA-Z0-9]` |
| `HEX_DIGIT` | `[0-9a-fA-F]` |

**Example usage:**
```python
ONE_OR_MORE(HEX_DIGIT)   # -> "[0-9a-fA-F]+"
```

[▲ Back to top](#-table-of-contents)

---

### `literals`

Control-character `Literal` presets — wrap the real control character (not the
two-character escape *text*), since `re.escape` handles the rendering correctly
either way; these exist purely because the characters themselves are invisible/easy
to mistype at a call site.

| Preset | Character |
|---|---|
| `TAB` | tab |
| `NEWLINE` | newline |
| `CARRIAGE_RETURN` | carriage return |
| `FORM_FEED` | form feed |
| `VERTICAL_TAB` | vertical tab |
| `BELL` | bell |
| `BACKSLASH_CHAR` | a literal `\` |

**Example usage:**
```python
Sequence(Literal("a"), TAB, Literal("b")).to_pattern()   # matches "a<TAB>b"
```

[▲ Back to top](#-table-of-contents)

---

### `quantifiers`

Factory functions over `Repeat` — see
[`README_REGEX_CONTAINERS`](README_REGEX_CONTAINERS.md#repeat).

| Preset | Signature | Renders (example) |
|---|---|---|
| `OPTIONAL` | `(inner)` | `inner?` |
| `ZERO_OR_MORE` | `(inner, *, mode=GREEDY)` | `inner*` |
| `ONE_OR_MORE` | `(inner, *, mode=GREEDY)` | `inner+` |
| `EXACTLY` | `(inner, count)` | `inner{count}` |
| `AT_LEAST` | `(inner, count, *, mode=GREEDY)` | `inner{count,}` |
| `BETWEEN` | `(inner, min_count, max_count, *, mode=GREEDY)` | `inner{min,max}` |

**Example usage:**
```python
EXACTLY(Literal("ab"), 3)         # -> "(?:ab){3}"
BETWEEN(DIGIT, 2, 4, mode=RepeatMode.POSSESSIVE)   # -> "\d{2,4}+"
```

[▲ Back to top](#-table-of-contents)

---

### `groups`

Factory functions over `Group` — see
[`README_REGEX_CONTAINERS`](README_REGEX_CONTAINERS.md#group) and
[`README_REGEX_FLAGS`](README_REGEX_FLAGS.md) for the underlying `Flag` reference.

| Preset | Signature | Renders (example) |
|---|---|---|
| `NAMED_GROUP` | `(inner, name)` | `(?P<name>inner)` |
| `NON_CAPTURING` | `(inner)` | `(?:inner)` |
| `ATOMIC_GROUP` | `(inner)` | `(?>inner)` |
| `WITH_FLAGS` | `(inner, *flags)` | `(?flags:inner)` — generic fallback for any flag combination without its own named preset |
| `CASE_INSENSITIVE` | `(inner)` | `(?i:inner)` |
| `VERBOSE_GROUP` | `(inner)` | `(?x:inner)` |

**Example usage:**
```python
NAMED_GROUP(ONE_OR_MORE(DIGIT), "year")             # -> "(?P<year>\d+)"
WITH_FLAGS(ONE_OR_MORE(DIGIT), Flag.MULTILINE, Flag.DOTALL)   # -> "(?ms:\d+)"
```

[▲ Back to top](#-table-of-contents)

---

### `lookaround`

Factory functions over `Lookaround` — see
[`README_REGEX_CONTAINERS`](README_REGEX_CONTAINERS.md#lookaround).

| Preset | Signature | Renders (example) |
|---|---|---|
| `LOOKAHEAD` | `(inner)` | `(?=inner)` |
| `NEGATIVE_LOOKAHEAD` | `(inner)` | `(?!inner)` |
| `LOOKBEHIND` | `(inner)` | `(?<=inner)` — `inner` must have a fixed length |
| `NEGATIVE_LOOKBEHIND` | `(inner)` | `(?<!inner)` — `inner` must have a fixed length |

**Example usage:**
```python
LOOKBEHIND(Literal("USD")) + ONE_OR_MORE(DIGIT)   # -> "(?<=USD)\d+"
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#presets--ready-made-instances--factories)
