# 🚩 `regex/flags` — Inline & Compile-Time Regex Flags

The `flags` package holds a single `Enum`, `Flag` — the seven inline regex flags
Python's `re` recognizes, usable either scoped to one `Group` (`flags=`/`flags_off=`)
or globally at `RegexPattern.compile()` time. `Flag` is deliberately NOT a `Regex`
node itself: a flag has no `to_pattern`/`fixed_length` of its own, it only ever
appears as a *parameter* to something else.

```python
from enum import Enum


class Flag(Enum):
    ...
```

---

## 🧭 Table of Contents

* [`Flag`](#flag)
* [Restrictions](#restrictions)

[⬅️ Back to main README](../README.md#flags--inline--compile-time-flags)

---

### `Flag`

**Members and inline letters:**

| Member | Letter | `re` module flag |
|---|---|---|
| `ASCII` | `a` | `re.ASCII` |
| `IGNORECASE` | `i` | `re.IGNORECASE` |
| `LOCALE` | `L` | `re.LOCALE` |
| `MULTILINE` | `m` | `re.MULTILINE` |
| `DOTALL` | `s` | `re.DOTALL` |
| `UNICODE` | `u` | `re.UNICODE` |
| `VERBOSE` | `x` | `re.VERBOSE` |

**Properties:**
* `.re_flag` (*re.RegexFlag*): The corresponding `re` module flag — used by
  `RegexPattern` to OR every requested `Flag` together for top-level compilation.

**Example usage:**
```python
Group(DIGIT, capturing=False, flags={Flag.IGNORECASE})   # -> "(?i:\d)"
RegexPattern(pattern, flags=frozenset({Flag.MULTILINE}))
```

`re.DEBUG` and `re.NOFLAG` are deliberately excluded — `DEBUG` has no inline form at
all, and `NOFLAG` is just the value `0`, never something a caller composes with
others.

[▲ Back to top](#-table-of-contents)

---

## Restrictions

Four restrictions, both verified directly against `re.compile` and enforced at
construction time by `Group` and `RegexPattern` alike — a caller never discovers
either only later, inside `re.compile()`:

* **`Flag.LOCALE` cannot be used with a `str` pattern at all** (`re` raises `cannot
  use LOCALE flag with a str pattern`). Since this library only ever compiles `str`
  patterns, `Flag.LOCALE` is rejected outright — in `Group(..., flags=...)` and in
  `RegexPattern(..., flags=...)` alike.
* **Only `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE` can ever be turned OFF** in a
  scoped `Group`'s `flags_off` — Python's `re` rejects `ASCII`/`LOCALE`/`UNICODE`
  there (`cannot turn off flags 'a', 'u' and 'L'`), since those three can only ever
  be turned ON.
* **The same flag cannot be enabled and disabled simultaneously in the same group** ((?i-i:...)).
* **`ASCII` and `UNICODE` cannot be enabled together.**

```python
Group(DIGIT, capturing=False, flags={Flag.IGNORECASE}, flags_off={Flag.ASCII})
# -> raises: ASCII can never be turned off

RegexPattern(pattern, flags=frozenset({Flag.LOCALE}))
# -> raises: LOCALE cannot be used with a str pattern
```

Combinations only `re.compile` can judge — such as `ASCII` together with `UNICODE` — are
reported by `RegexPattern` as `INVALID_PATTERN_ERROR`.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#flags--inline--compile-time-flags)
