# 🔤 `regex/elements` — Leaves of the Pattern Tree

The `elements` package holds every node that represents a piece of matchable content
directly, rather than combining other nodes — the leaves every `containers/` node
eventually bottoms out at. Several unify a whole syntax family the same way
`containers/`'s `Repeat`/`Group`/`Lookaround` do (`Anchor` covers 6+ position
assertions, `CharacterType` covers 6 built-in classes, `CharCode` covers 5 escape
syntaxes) via one parameterized class plus a `Kind` enum.

```python
from ..base_class import Regex

class Literal(Regex):
    ...
```

## A note on `_usable_in_char_class`

Every atom either can or cannot appear as a standalone item inside a `CharacterClass`
(`[...]`) — and the two contexts sometimes give identical syntax completely different
meanings (`\1` outside a class is a backreference; inside one, an octal escape). Each
card below states this explicitly. `CharacterClass` itself is the single enforcement
point: it checks `_usable_in_char_class` on every item it receives, so an atom that
doesn't belong there (`Anchor`, `GroupReference`) is rejected at construction, not
silently compiled into something misleading.

---

## 🧭 Table of Contents

* [`Literal`](#literal)
* [`RawPattern`](#rawpattern)
* [`Anchor`](#anchor)
* [`AnyCharacter`](#anycharacter)
* [`CharacterType`](#charactertype)
* [`CharacterRange`](#characterrange)
* [`CharacterClass`](#characterclass)
* [`GroupReference`](#groupreference)
* [`CharCode`](#charcode)

[⬅️ Back to main README](../README.md#elements--leaves-of-the-tree)

---

### `Literal`

Matches the given text literally, character for character, auto-escaping every
regex-special character via `re.escape`.

**Parameters:**
* `text` (*str*): The literal text. Must be non-empty.

**Usable in a `CharacterClass`:** only when exactly one character long — a longer
`Literal` is rejected by `CharacterClass.__init__` (`[ab]` means "a or b," never the
substring "ab").

**Example usage:**
```python
Literal("a.b")      # -> "a\.b"     (matches the literal string "a.b")
Literal(".")         # -> "\."
```

**Under the hood** *(`to_pattern`)*:
```python
def to_pattern(self) -> str:
    return re.escape(self.text)
```

`fixed_length` is always `len(text)`. A multi-character `Literal` also signals
`needs_wrap_for_repeat() == True`, so `Repeat` wraps it correctly (see
[`README_REGEX_CLASS`](README_REGEX_CLASS.md#needs_wrap_for_repeat)).

[▲ Back to top](#-table-of-contents)

---

### `RawPattern`

Escape hatch for raw regex syntax the DSL does not (yet) express as its own node —
the text is inserted UNCHANGED, with no escaping. The deliberate opposite of
`Literal`: `Literal` promises "this text, matched literally" (escaped); `RawPattern`
promises "this regex syntax, trust me" (verbatim).

**Parameters:**
* `text` (*str*): Raw regex syntax. Must be non-empty.

**Usable in a `CharacterClass`:** never — the escaping rules inside `[...]` (Point 4)
cannot be verified for opaque text.

**Example usage:**
```python
Literal("b.c").to_pattern()       # -> "b\.c"   — doslovný text
RawPattern("b.c").to_pattern()    # -> "b.c"    — "cokoliv" + "c", beze změny
```

**Under the hood** *(`to_pattern`)*:
```python
def to_pattern(self) -> str:
    return self.text
```

Every capability defaults to the safest possible answer, since a `RawPattern`'s
actual internal structure is unknowable without parsing it: `_precedence` is always
`ALTERNATION` (always wrapped in `(?:...)` when embedded — safe even if the text
turns out not to need it), and `fixed_length()` is unconditionally `None` (so a
`RawPattern` is always rejected inside `Lookaround(direction=BEHIND)`, rather than
risking a wrong guess about its width).

```python
Lookaround(RawPattern(r"\d{3}"), direction=LookaroundDirection.BEHIND)
# -> raises, even though "\d{3}" genuinely has a fixed length — RawPattern
#    has no way to know that without parsing, so it declines rather than guesses
```

[▲ Back to top](#-table-of-contents)

---

### `Anchor`

A zero-width position assertion — matches a position, not a character.

**Parameters:**
* `kind` (*AnchorKind*): Which assertion.

**`AnchorKind` values:**

| Member              | Syntax | Meaning                                                 |
|---------------------|--------|---------------------------------------------------------|
| `START`             | `^`    | Start of string (or line, under `MULTILINE`)            |
| `END`               | `$`    | End of string (or line, under `MULTILINE`)              |
| `START_STRING`      | `\A`   | Start of the whole string, always                       |
| `END_STRING`        | `\Z`   | End of the whole string, always — works on Python 3.11+ |
| `END_STRING_PY314`  | `\z`   | Same meaning as `END_STRING`, **Python 3.14+ only**     |
| `WORD_BOUNDARY`     | `\b`   | Between a word/non-word character                       |
| `NON_WORD_BOUNDARY` | `\B`   | Not a word boundary                                     |

**Usable in a `CharacterClass`:** never — an anchor has no meaning inside `[...]`.

**Example usage:**
```python
Anchor(AnchorKind.START_STRING)   # -> "\A"
START                             # preset, see README_REGEX_PRESETS
```

**Raises:**
* `ValueError`: Constructing `Anchor(AnchorKind.END_STRING_PY314)` on an interpreter
  below Python 3.14 fails immediately, naming the version requirement and pointing
  at `END_STRING` (`\Z`) as the drop-in replacement — never deferred to `re.compile`'s
  much less specific `bad escape \z`.

`fixed_length` is unconditionally `0` — every anchor is zero-width by definition.

[▲ Back to top](#-table-of-contents)

---

### `AnyCharacter`

Matches any single character except newline (or, under `DOTALL`, truly any
character). Stateless and parameterless — exposed as a single shared instance (`ANY`)
rather than something constructed repeatedly.

**Parameters:**
* *(none)*

**Usable in a `CharacterClass`:** never — `[.]` inside a class means the *literal*
character `.`, an entirely different meaning from "any character." Use `Literal(".")`
for that.

**Example usage:**
```python
ANY.to_pattern()   # -> "."
```

`fixed_length` is unconditionally `1`.

[▲ Back to top](#-table-of-contents)

---

### `CharacterType`

A single character matching a built-in Unicode character class.

**Parameters:**
* `kind` (*CharacterTypeKind*): Which class.

**`CharacterTypeKind` values:** `DIGIT` (`\d`), `NON_DIGIT` (`\D`), `WORD` (`\w`),
`NON_WORD` (`\W`), `WHITESPACE` (`\s`), `NON_WHITESPACE` (`\S`).

**Usable in a `CharacterClass`:** always — these six retain their outside-the-class
meaning when placed inside one (`[\d\s]` really does mean "a digit or whitespace").

**Example usage:**
```python
CharacterType(CharacterTypeKind.DIGIT)   # -> "\d"
DIGIT                                     # preset, see README_REGEX_PRESETS
CharacterClass(DIGIT, WHITESPACE)         # -> "[\d\s]"
```

`fixed_length` is unconditionally `1`.

[▲ Back to top](#-table-of-contents)

---

### `CharacterRange`

A contiguous range of characters, e.g. `a-z`. Only ever legal as a standalone item
inside a `CharacterClass` — a range has no standalone meaning outside `[...]`.

**Parameters:**
* `start` (*str*): A single character.
* `end` (*str*): A single character. Must not come before `start`.

**Usable in a `CharacterClass`:** yes — this is its only legal context.

**Example usage:**
```python
CharacterClass(CharacterRange("a", "z"))   # -> "[a-z]"
```

**Raises:**
* `TypeError`: Calling `.to_pattern()` directly (outside a `CharacterClass`) always
  raises — there is no meaningful standalone rendering for a bare range.

`fixed_length` is `1`, for consistency, though this is only ever meaningful inside a
`CharacterClass`, which already reports `1` for itself regardless of its items.

[▲ Back to top](#-table-of-contents)

---

### `CharacterClass`

Matches exactly one character, chosen from (or excluded from) the given set of items.
Only accepts items where `_usable_in_char_class` is `True`.

**Parameters:**
* `*items` (*Regex*): One or more items — a single-character `Literal`, a
  `CharacterType`, a `CharacterRange`, or a `CharCode`. At least one required.
* `negate` (*bool*, keyword-only, default `False`): `[^...]` instead of `[...]`.

**Example usage:**
```python
CharacterClass(Literal("a"), Literal("b"), Literal("c"))   # -> "[abc]"
CharacterClass(CharacterRange("a", "z"), negate=True)       # -> "[^a-z]"
CharacterClass(DIGIT, WHITESPACE)                            # -> "[\d\s]"
```

**Raises:**
* `TypeError`: Any item with `_usable_in_char_class = False` (e.g. `Anchor`, `ANY`,
  `GroupReference`) is rejected outright.
* `ValueError`: A multi-character `Literal` item is rejected (see `Literal` above).

**Under the hood** *(`to_pattern`)*:
```python
def to_pattern(self) -> str:
    content = "".join(item.to_char_class_fragment() for item in self.items)
    return f"{'[^' if self.negate else '['}{content}]"
```

Every item renders via `to_char_class_fragment()`, never `to_pattern()` directly —
see [`README_REGEX_CLASS`](README_REGEX_CLASS.md#to_char_class_fragment). `re`
supports no nesting of one class inside another; `CharacterClass` simply never sets
its own `_usable_in_char_class = True`, so this is rejected by the ordinary item
check with no special-case code. `fixed_length` is unconditionally `1`.

[▲ Back to top](#-table-of-contents)

---

### `GroupReference`

Backreference to a previously captured group, by number or name.

**Parameters:**
* `id_or_name` (*int | str*): A 1-based numeric id, or a group name.

**Usable in a `CharacterClass`:** never — `\1` inside `[...]` is an octal escape, a
genuinely different meaning from a backreference.

**Example usage:**
```python
GroupReference(1)          # -> "\1"
GroupReference("year")     # -> "(?P=year)"
```

`fixed_length` is unconditionally `None` — a backreference's width depends entirely
on what the referenced group actually captured at runtime, which a static tree has no
way to know.

[▲ Back to top](#-table-of-contents)

---

### `CharCode`

A single character specified by numeric code or Unicode name — unifies 5 escape
syntaxes into one mechanism.

**Parameters:**
* `kind` (*CharCodeKind*): Which syntax.
* `value` (*int | str*): The code (int, range-checked per `kind`) or name (str, for
  `NAMED`).

**`CharCodeKind` values and ranges:**

| Member | Syntax | Value range |
|---|---|---|
| `HEX` | `\xFF` | `0x00`–`0xFF` |
| `UNICODE_SHORT` | `\uFFFF` | `0x0000`–`0xFFFF` |
| `UNICODE_LONG` | `\U0010FFFF` | `0x000000`–`0x10FFFF` |
| `NAMED` | `\N{NAME}` | any non-empty `str` |
| `OCTAL` | `\ooo` | `0`–`0o377` (verified against `re.compile`; `0o400`+ is rejected) |

**Usable in a `CharacterClass`:** always — all five mean the same thing inside and
outside `[...]`.

**Example usage:**
```python
CharCode(CharCodeKind.HEX, 0x41)          # -> "\x41"  (matches "A")
CharCode(CharCodeKind.NAMED, "BULLET")     # -> "\N{BULLET}"
```

**Raises:**
* `ValueError`: A `value` outside the kind's range (e.g. `CharCode(HEX, 300)`).

Octal renders zero-padded to exactly 3 digits (`\001`, never bare `\1`) to avoid any
ambiguity with backreferences. `fixed_length` is unconditionally `1`.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#elements--leaves-of-the-tree)
