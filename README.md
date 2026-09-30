# 🧬 `simplibs-regex`

[![PyPI](https://img.shields.io/pypi/v/simplibs-regex)](https://pypi.org/project/simplibs-regex/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-regex/blob/main/LICENSE)

**Compose regular expressions as Python code — no regex syntax required.**

A lightweight Python library that lets you build regular expressions out of small,
composable `Regex` objects instead of a raw pattern string. Nodes combine with plain
Python operators (`+`, `|`) and constructors, each syntax *family* Python's `re`
supports (quantifiers, groups, lookarounds) collapses into one parameterized
mechanism instead of dozens of special cases, and the whole tree compiles down to a
real, ordinary `re.Pattern` when you're done.

```python
from simplibs.regex.elements import Literal
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.quantifiers import ONE_OR_MORE
from simplibs.regex.presets.groups import NAMED_GROUP
from simplibs.regex.compiler import RegexPattern

year = NAMED_GROUP(ONE_OR_MORE(DIGIT), "year")
pattern = Literal("born:") + Literal(" ") + year

compiled = RegexPattern(pattern)
compiled.search("Born: 2026 in Prague").group("year")  # -> "2026"
```

> `simplibs-regex` builds directly on the same architectural pattern as
> [`simplibs-rules`](https://pypi.org/project/simplibs-rules/) (a `Rule` base class +
> composable containers + presets) and
> [`simplibs-actions`](https://pypi.org/project/simplibs-actions/) — if either of
> those is familiar, this library's shape will be too.

---

## 🧭 The Core Philosophy

Writing a raw regex string means holding an entire, terse, write-only syntax in your
head at once — precedence rules, six different group syntaxes, escape sequences that
mean different things inside `[...]` than outside it. `simplibs-regex` replaces that
string with a small tree of ordinary Python objects: each node is independently
named, typed, and validated, and the tree composes with `+` (concatenation) and `|`
(alternation) the same way arithmetic expressions do.

Every syntax *family* — not just every syntax — is represented by exactly one
mechanism. Fourteen quantifier spellings (`*` `+` `?` `{n}` `{n,}` `{m,n}` ×
greedy/lazy/possessive) become one `Repeat(min, max, mode)`. Six group spellings
become one `Group(capturing, name, atomic, flags, flags_off)`. Four lookaround
spellings become one `Lookaround(direction, negate)`. This is deliberate: the goal is
never to add a new class for every distinct piece of regex syntax, but to find the
smallest set of genuinely different *mechanisms* and expose every syntax variant as a
parameter or a named preset on top of one of them.

```python
Repeat(Literal("ab"), min=3, max=3)                  # -> "(?:ab){3}"
Group(DIGIT, name="year")                             # -> "(?P<year>\d)"
Lookaround(Literal("USD"), direction=BEHIND)           # -> "(?<=USD)"
```

Invalid combinations are rejected the moment you try to build them — a
variable-length lookbehind, a `Group` that tries to be both named and flag-scoped, a
`CharacterClass` item that doesn't belong there — rather than compiling into
something that only fails later, confusingly, inside `re.compile()`.

---

## 📦 Installation

```bash
pip install simplibs-regex
```

---

## 🚀 Quick Start in 60 Seconds

### Level 1: Build a tree, get a pattern string

```python
from simplibs.regex.elements import Literal
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.quantifiers import ONE_OR_MORE

phone = Literal("+1-") + ONE_OR_MORE(DIGIT)
phone.to_pattern()   # -> "\+1\-\d+"
```

### Level 2: Compile and use it like any `re.Pattern`

```python
from simplibs.regex.compiler import RegexPattern

pattern = RegexPattern(phone)
pattern.search("call +1-5551234")  # -> a re.Match object
pattern.findall("+1-111 and +1-222")  # -> ["111", "222"]
```

### Level 3: Compose groups, quantifiers, and lookarounds together

```python
from simplibs.regex.presets.groups import NAMED_GROUP
from simplibs.regex.presets.lookaround import LOOKBEHIND
from simplibs.regex.presets.quantifiers import ONE_OR_MORE
from simplibs.regex.flags.Flag import Flag

price = LOOKBEHIND(Literal("$")) + NAMED_GROUP(ONE_OR_MORE(DIGIT), "amount")
pattern = RegexPattern(price, flags=frozenset({Flag.MULTILINE}))
pattern.search("Total: $42").group("amount")   # -> "42"
```

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/regex/
├── base_class/            ◄── Abstract base class Regex & precedence-aware rendering
│   ├── Regex.py
│   └── _Precedence.py
├── compiler/              ◄── RegexPattern — the compiled, ready-to-use runtime wrapper
├── containers/            ◄── Nodes that combine other nodes (Sequence, Alternation,
│                              Repeat, Group, Lookaround, Conditional)
├── elements/              ◄── Leaves of the tree (Literal, RawPattern, Anchor, AnyCharacter,
│                              CharacterType, CharacterRange, CharacterClass, GroupReference, CharCode)
├── flags/                 ◄── The Flag enum (inline & compile-time regex flags)
└── presets/               ◄── Ready-made instances & factory functions over containers/elements 
                               (anchors, character_types, character_classes, literals, quantifiers, 
                               groups, lookaround, any_character)
```

---

## 🧩 The `Regex` Class

Every node in this library inherits from `Regex`. It defines the mandatory contract
(`to_pattern`), precedence-aware rendering, fixed-length introspection, and `+`/`|`
composition out of the box.

```python
class Regex(ABC):

    @abstractmethod
    def to_pattern(self) -> str:
        """Return this node's own regex fragment."""
        raise NotImplementedError

    def fixed_length(self) -> int | None:
        """Return this node's match width if fixed, else None."""
        return None

    def render(self, parent_precedence: "_Precedence") -> str:
        """Render for embedding, wrapping in (?:...) exactly when needed."""
        ...

    def __add__(self, other: "Regex") -> "Regex": ...   # -> Sequence
    def __or__(self, other: "Regex") -> "Regex": ...    # -> Alternation
```

➡️ Full method-by-method reference: [README_REGEX_CLASS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_CLASS.md)

---

## 📖 Quick Reference

### `containers/` — Combining nodes

| Class         | Description / Parameters                                                           |
|---------------|------------------------------------------------------------------------------------|
| `Sequence`    | Concatenation (`*nodes`). Behind `+`.                                              |
| `Alternation` | Logical OR (`*nodes`). Behind `\|`.                                                |
| `Repeat`      | Unifies all 14 quantifier syntaxes (`inner, min, max, mode`).                      |
| `Group`       | Unifies all 6 group syntaxes (`inner, capturing, name, atomic, flags, flags_off`). |
| `Lookaround`  | Unifies all 4 lookaround syntaxes (`inner, direction, negate`).                    |
| `Conditional` | Group-existence branching (`id_or_name, yes, no`).                                 |

➡️ [README_REGEX_CONTAINERS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_CONTAINERS.md)

### `elements/` — Leaves of the tree

| Class            | Description                                                      |
|------------------|------------------------------------------------------------------|
| `Literal`        | Literal text, auto-escaped.                                      |
| `RawPattern`     | Escape hatch for raw regex syntax with no dedicated node yet.    |
| `Anchor`         | Zero-width position assertions (`^ $ \A \Z \z\* \b \B`).         |
| `AnyCharacter`   | The `.` wildcard.                                                |
| `CharacterType`  | Built-in classes (`\d \D \w \W \s \S`).                          |
| `CharacterRange` | `a-z`-style ranges — only inside `CharacterClass`.               |
| `CharacterClass` | `[...]` / `[^...]`.                                              |
| `GroupReference` | Backreferences (`\1`, `(?P=name)`).                              |
| `CharCode`       | Character-code escapes (`\xFF \uFFFF \Uhhhhhhhh \N{name} \ooo`). |

*\* `\z` requires Python 3.14+; see [README_REGEX_ELEMENTS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_ELEMENTS.md#anchor).*

➡️ [README_REGEX_ELEMENTS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_ELEMENTS.md)

### `flags/` — Inline & compile-time flags

`Flag` — `ASCII`, `IGNORECASE`, `LOCALE`, `MULTILINE`, `DOTALL`, `UNICODE`,
`VERBOSE` — with the restrictions Python's `re` actually enforces (`LOCALE` unusable
with `str` patterns, only `imsx` can be turned off in a scoped group) validated at
construction time, not deferred to `re.compile()`.

➡️ [README_REGEX_FLAGS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_FLAGS.md)

### `compiler/` — Compiled runtime wrapper

`RegexPattern` — compiles a tree once, then exposes `search`/`match`/`fullmatch`/
`findall`/`finditer`/`sub`/`subn`/`split`, thin delegation to the underlying
`re.Pattern`.

➡️ [README_REGEX_COMPILER](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_COMPILER.md)

### `presets/` — Ready-made instances & factories

* **`anchors`**: `START`, `END`, `START_STRING`, `END_STRING`, `WORD_BOUNDARY`, `NON_WORD_BOUNDARY`
* **`any_character`**: `ANY`
* **`character_types`**: `DIGIT`, `NON_DIGIT`, `WORD`, `NON_WORD`, `WHITESPACE`, `NON_WHITESPACE`
* **`character_classes`**: `LOWERCASE_LETTER`, `UPPERCASE_LETTER`, `LETTER`, `ALPHANUMERIC`, `HEX_DIGIT`
* **`literals`**: `TAB`, `NEWLINE`, `CARRIAGE_RETURN`, `FORM_FEED`, `VERTICAL_TAB`, `BELL`, `BACKSLASH_CHAR`
* **`quantifiers`**: `OPTIONAL`, `ZERO_OR_MORE`, `ONE_OR_MORE`, `EXACTLY`, `AT_LEAST`, `BETWEEN`
* **`groups`**: `NAMED_GROUP`, `NON_CAPTURING`, `ATOMIC_GROUP`, `WITH_FLAGS`, `CASE_INSENSITIVE`, `VERBOSE_GROUP`
* **`lookaround`**: `LOOKAHEAD`, `NEGATIVE_LOOKAHEAD`, `LOOKBEHIND`, `NEGATIVE_LOOKBEHIND`

➡️ [README_REGEX_PRESETS](https://github.com/simplibs/simplibs-regex/blob/main/docs/README_REGEX_PRESETS.md)

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---

[▲ Back to Top](#-simplibs-regex)
