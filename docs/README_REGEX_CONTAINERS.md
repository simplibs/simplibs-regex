# 📦 `regex/containers` — Composable Pattern Containers

The `containers` package holds every node that combines *other* nodes into a larger
pattern — the connective tissue that turns individual atoms (`Literal`, `DIGIT`,
`Anchor`) into arbitrarily complex regexes. This is also where `Regex`'s two
composition operators (`+`, `|`) resolve to, and where every syntax *family* in
Python's `re` — quantifiers, groups, lookarounds — collapses into one parameterized
mechanism instead of one class per syntax variant.

```python
from ..base_class import Regex

class Sequence(Regex):
    ...
```

## A note on the "one mechanism, many syntaxes" pattern

Three containers here each unify what would otherwise be many separate constructs:
`Repeat` collapses 14 quantifier syntaxes (`*` `+` `?` `{n}` `{n,}` `{m,n}` ×
greedy/lazy/possessive) into `min`/`max`/`mode`; `Group` collapses 6 group syntaxes
(`()`, `(?:)`, `(?P<name>)`, `(?>)`, `(?flags:)`, `(?flags-flags:)`) into
`capturing`/`name`/`atomic`/`flags`/`flags_off`; `Lookaround` collapses 4 assertion
syntaxes into `direction`/`negate`. Every one of these three validates its own
parameter combinations at construction time — an invalid combination (a variable-length
lookbehind, a scoped-flag group that also tries to be named, a `flags_off` letter
Python's `re` never allows to be turned off) raises immediately, with a message naming
exactly what's wrong, rather than surfacing later as a cryptic `re.error`.

---

## 🧭 Table of Contents

* [`Sequence`](#sequence)
* [`Alternation`](#alternation)
* [`Repeat`](#repeat)
* [`Group`](#group)
* [`Lookaround`](#lookaround)
* [`Conditional`](#conditional)

[⬅️ Back to main README](../README.md#containers--composing-nodes)

---

### `Sequence`

Concatenation of nodes — node1 followed by node2 followed by ... — the container
behind the `+` operator. Rejects construction with zero nodes, and self-flattens any
nested `Sequence` passed among its arguments, so `a + b + c` produces one flat
`Sequence(a, b, c)` rather than a needlessly nested one.

**Parameters:**
* `*nodes` (*Regex*): One or more nodes. At least one is required.

**Example usage:**
```python
Sequence(Literal("ab"), DIGIT)      # -> "ab\d"
Literal("ab") + DIGIT               # equivalent, via the + operator
```

**Under the hood** *(`to_pattern`)*:
```python
def to_pattern(self) -> str:
    return "".join(node.render(self._precedence) for node in self.nodes)
```

`fixed_length` sums every child's own fixed length, bailing to `None` the moment any
child is variable.

[▲ Back to top](#-table-of-contents)

---

### `Alternation`

Match any ONE of the given nodes — the container behind the `|` operator. Same
construction-time guard and self-flattening behavior as `Sequence`, mirrored for
`|`-chained expressions.

**Parameters:**
* `*nodes` (*Regex*): One or more nodes. At least one is required.

**Example usage:**
```python
Alternation(Literal("cat"), Literal("dog"))   # -> "cat|dog"
Literal("cat") | Literal("dog")                # equivalent, via the | operator
```

**Under the hood** *(`to_pattern`)*:
```python
def to_pattern(self) -> str:
    return "|".join(node.render(self._precedence) for node in self.nodes)
```

`fixed_length` returns the shared length only if EVERY branch has the exact same
fixed length (Python's `re` accepts this shape inside a lookbehind — `(?<=cat|dog)`
is valid because both branches are 3 characters wide) — otherwise `None`.

[▲ Back to top](#-table-of-contents)

---

### `Repeat`

Repeats the inner node between `min` and `max` times — unifies all 14 Python `re`
quantifier syntaxes into one mechanism.

**Parameters:**
* `inner` (*Regex*): The node to repeat.
* `min` (*int*, keyword-only, default `0`): Minimum repetitions. Must be `>= 0`.
* `max` (*int | None*, keyword-only, default `None`): Maximum repetitions, or `None`
  for unbounded. Must be `>= min` if given.
* `mode` (*RepeatMode*, keyword-only, default `RepeatMode.GREEDY`): `GREEDY`, `LAZY`,
  or `POSSESSIVE` (3.11+).

**Example usage:**
```python
Repeat(DIGIT, min=0, max=None)                        # -> "\d*"
Repeat(DIGIT, min=1, max=None, mode=RepeatMode.LAZY)   # -> "\d+?"
Repeat(Literal("ab"), min=3, max=3)                    # -> "(?:ab){3}"
```

**Under the hood** *(quantifier shorthand selection)*:
```python
def _build_quantifier(self) -> str:
    if self.min == 0 and self.max is None:
        return "*"
    if self.min == 1 and self.max is None:
        return "+"
    if self.min == 0 and self.max == 1:
        return "?"
    if self.min == self.max:
        return f"{{{self.min}}}"
    if self.max is None:
        return f"{{{self.min},}}"
    return f"{{{self.min},{self.max}}}"
```

A multi-character `Literal` passed as `inner` is automatically wrapped in `(?:...)`
(via `needs_wrap_for_repeat`) so the quantifier applies to the whole literal, not just
its last character. Any other inner that is not a single token (`Sequence`,
`Alternation`, another `Repeat`) is wrapped too, e.g.
`Repeat(Repeat(DIGIT), min=3, max=3)` -> `(?:\d*){3}`. An `Anchor` cannot be repeated directly (`re` rejects `^*` and `\b?` with
"nothing to repeat"), so `Repeat` raises on it; wrap it in a `Group` if you really need to.
`fixed_length` returns `min * inner_length` only when `min ==
max` and `inner` itself has a fixed length (with `{0}` always reporting `0`,
regardless of `inner`).

[▲ Back to top](#-table-of-contents)

---

### `Group`

A parenthesized group around `inner` — unifies 6 group syntaxes into one mechanism.

**Parameters:**
* `inner` (*Regex*): The node to group.
* `capturing` (*bool*, keyword-only, default `True`): Whether the group captures.
* `name` (*str | None*, keyword-only, default `None`): A capture-group name. Requires
  `capturing=True`.
* `atomic` (*bool*, keyword-only, default `False`): No backtracking into the group.
  Mutually exclusive with `name` and `flags`/`flags_off`.
* `flags` (*set[Flag] | frozenset[Flag] | None*, keyword-only): Flags scoped to `inner` only.
  Requires `capturing=False`. Mutually exclusive with `name`/`atomic`.
* `flags_off` (*set[Flag] | frozenset[Flag] | None*, keyword-only): Flags explicitly turned off
  inside the scope. Requires `flags` to also be given, and may only contain
  `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE` — Python's `re` never allows `ASCII`,
  `LOCALE`, or `UNICODE` to be turned off. `Flag.LOCALE` in `flags` is rejected
  outright, since it cannot be used with a `str` pattern at all. 
  The same flag cannot be present in both `flags` and `flags_off`. 
  `ASCII` and `UNICODE` cannot be combined within `flags`.

**Example usage:**
```python
Group(DIGIT)                                    # -> "(\d)"
Group(DIGIT, capturing=False)                    # -> "(?:\d)"
Group(DIGIT, name="year")                        # -> "(?P<year>\d)"
Group(DIGIT, atomic=True)                        # -> "(?>\d)"
Group(DIGIT, capturing=False, flags={Flag.IGNORECASE})   # -> "(?i:\d)"
```

**Under the hood** *(opening-syntax selection)*:
```python
def _build_opening(self) -> str:
    if self.atomic:
        return "(?>"
    if self.name is not None:
        return f"(?P<{self.name}>"
    if self.flags or self.flags_off:
        on = "".join(sorted(f.value for f in self.flags))
        off = "".join(sorted(f.value for f in self.flags_off))
        return f"(?{on}{'-' + off if off else ''}:"
    if not self.capturing:
        return "(?:"
    return "("
```

`fixed_length` is pure delegation to `inner.fixed_length()` — a group is transparent
to match width regardless of capturing/flag behavior. See
[`README_REGEX_FLAGS`](README_REGEX_FLAGS.md) for the full `Flag` reference and
restrictions.

[▲ Back to top](#-table-of-contents)

---

### `Lookaround`

Zero-width assertion that `inner` does (or does not) match at the current position —
unifies all 4 lookaround syntaxes into one mechanism.

**Parameters:**
* `inner` (*Regex*): The node to assert.
* `direction` (*LookaroundDirection*, keyword-only): `AHEAD` or `BEHIND`.
* `negate` (*bool*, keyword-only, default `False`): Negates the assertion.

**Example usage:**
```python
Lookaround(DIGIT, direction=LookaroundDirection.AHEAD)            # -> "(?=\d)"
Lookaround(Literal("USD"), direction=LookaroundDirection.BEHIND)  # -> "(?<=USD)"
```

**Raises:**
* `ValueError`: If `direction=BEHIND` and `inner.fixed_length()` is `None` — Python's
  `re` cannot compile a variable-length lookbehind, and this is caught here rather
  than deferred to `re.compile()`.

```python
LOOKBEHIND(ZERO_OR_MORE(DIGIT))   # -> raises: inner has no fixed length
LOOKBEHIND(Alternation(Literal("cat"), Literal("dog")))  # -> OK: both 3 chars wide
```

`fixed_length` is unconditionally `0` — every lookaround, like `Anchor`, consumes no
characters regardless of what `inner` matches against.

[▲ Back to top](#-table-of-contents)

---

### `Conditional`

Matches `yes` if the referenced group participated in the match so far, otherwise
matches `no` (or nothing, if `no` is omitted).

**Parameters:**
* `id_or_name` (*int | str*): The group to check — a 1-based numeric id or a name.
* `yes` (*Regex*): The branch to match if the group participated.
* `no` (*Regex | None*, default `None`): The branch to match otherwise.

**Example usage:**
```python
Conditional(1, Literal("a"), Literal("b"))   # -> "(?(1)a|b)"
Conditional("quoted", Literal('"'))          # -> "(?(quoted)\")"
```

A `yes`/`no` branch that is a `Sequence` or `Alternation` is wrapped in `(?:...)`, since
`re` allows only two branches: `Conditional(1, Literal("a") | Literal("b"))` ->
`(?(1)(?:a|b))`.

Unlike `Repeat`/`Group`/`Lookaround`, this has only one real syntax shape (with or
without a `no` branch), so it needs no internal mode enum — `no: Regex | None = None`
already captures the one variation point. `fixed_length` returns `None` when `no` is
omitted (the construct is, in effect, optional), or the shared length when both
branches agree — mirroring `Alternation`'s own rule.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#containers--composing-nodes)
