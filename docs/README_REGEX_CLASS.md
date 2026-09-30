# 🧩 `Regex` — Abstract Base Class for the Regex DSL

`Regex` is the single foundation every node in `simplibs-regex` is built on — from the
simplest atom (`Literal`, `Anchor`) to the most elaborate composed pattern
(`Sequence(Group(...), Repeat(...), Lookaround(...))`). It does not implement any
concrete regex construct itself; instead it provides four things every node needs:

1. A minimal, mandatory contract every concrete node must fulfill (`to_pattern`).
2. Precedence-aware rendering (`render`) so a composed tree wraps its own children in
   `(?:...)` exactly when needed — never more, never less — without any single
   container having to reason about every other container's syntax.
3. Fixed-length introspection (`fixed_length`) — the mechanism that lets `Lookaround`
   reject a variable-length lookbehind at construction time, instead of deferring to
   `re.compile()`'s far less specific error.
4. Operator-based composition (`+`, `|`) that lets any two nodes combine into a new
   node, without either side needing to know anything about the other.

```python
from abc import ABC, abstractmethod
from ._Precedence import _Precedence

class Regex(ABC):
    ...
```

## A note on why `Regex` is abstract

`Regex` can never be instantiated directly — `to_pattern` is declared with
`@abstractmethod` and carries no implementation of its own. This is deliberate:
`Regex` only defines *what every node must be able to produce* (its own regex
fragment), never *how* — that answer is always specific to the concrete node
(`Literal`, `Group`, `Repeat`, ...). Every piece of shared machinery this class *does*
provide (`render`, `compile`, the operators) is built purely on top of that one
abstract method, so any concrete node that implements it correctly gets the entire
rest of this interface for free.

---

## 🧭 Table of Contents

* [`to_pattern`](#to_pattern)
* [`fixed_length`](#fixed_length)
* [`render`](#render)
* [`needs_wrap_for_repeat`](#needs_wrap_for_repeat)
* [`to_char_class_fragment`](#to_char_class_fragment)
* [`compile`](#compile)
* [`__add__` / `__radd__`](#__add__--__radd__)
* [`__or__` / `__ror__`](#__or__--__ror__)
* [The `_Precedence` enum](#the-_precedence-enum)

[⬅️ Back to main README](../README.md#-the-regex-class)

---

### `to_pattern`

**Abstract.** The single true source of "what does this node look like as a regex
fragment" for every node in the library. Every other method that produces text —
`render`, `compile`, and every composed node's own `to_pattern` (`Sequence`,
`Group`, `Repeat`, ...) — ultimately reduces to calling this method somewhere.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `str`: This node's own regex fragment, WITHOUT any wrapping that depends on where
  it is embedded. Containers call `child.render(self._precedence)` on their children
  instead of `child.to_pattern()` directly, so wrapping decisions are made once, in
  one place (`render`), never duplicated per-container.

**Example usage:**
```python
Literal("abc").to_pattern()     # -> "abc"
DIGIT.to_pattern()               # -> "\d"
```

**Under the hood** *(as implemented by a concrete node, e.g. `Sequence`)*:
```python
def to_pattern(self) -> str:
    return "".join(node.render(self._precedence) for node in self.nodes)
```

[▲ Back to top](#-table-of-contents)

---

### `fixed_length`

Reports this node's match length in characters, if — and only if — it is fixed
regardless of input. The mechanism `Lookaround(direction=BEHIND)` uses to fail fast
at construction time when Python's `re` would otherwise reject a variable-length
lookbehind.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `int | None`: The fixed length, or `None` if unknown/variable. Defaults to `None`
  on `Regex` itself — a node that CAN determine a fixed length overrides this
  (`Literal` returns `len(text)`, `Sequence` sums its children or bails to `None` on
  the first variable one, `Alternation` returns the shared length only if every
  branch agrees, `Repeat` only when `min == max`, `Group`/`Conditional` delegate or
  compare branches, every zero-width node — `Anchor`, `Lookaround` itself,
  `CharacterClass` — returns a constant).

**Example usage:**
```python
Literal("USD").fixed_length()                    # -> 3
ZERO_OR_MORE(DIGIT).fixed_length()                # -> None (variable)
Alternation(Literal("cat"), Literal("dog")).fixed_length()  # -> 3 (same length)
```

**Under the hood** *(the base default)*:
```python
def fixed_length(self) -> int | None:
    return None
```

> ⚠️ Never guessed: returning a wrong non-`None` value here would let an invalid
> lookbehind slip past construction-time validation only to fail confusingly later,
> or silently compile something other than what was intended.

[▲ Back to top](#-table-of-contents)

---

### `render`

Renders this node for embedding inside a parent whose own binding power is
`parent_precedence` — the single, shared implementation of precedence-aware
wrapping every container in the library relies on.

**Parameters:**
* `parent_precedence` (*_Precedence*): The precedence level the parent is rendering
  its children at — almost always the parent's own `self._precedence` (`Sequence`,
  `Alternation`, `Repeat`), or the loosest level (`ALTERNATION`) for any node that
  already provides its own hard delimiters (`Group`, `Lookaround`, `Conditional`).

**Returns:**
* `str`: `to_pattern()`'s output, wrapped in `(?:...)` exactly when this node's own
  `_precedence` is strictly lower than `parent_precedence` — otherwise unchanged.

**Example usage:**
```python
alt = Alternation(Literal("cat"), Literal("dog"))
Sequence(Literal("a"), alt).to_pattern()   # -> "a(?:cat|dog)" — alt got wrapped
```

**Under the hood:**
```python
def render(self, parent_precedence: "_Precedence") -> str:
    fragment = self.to_pattern()
    if self._precedence < parent_precedence:
        return f"(?:{fragment})"
    return fragment
```

[▲ Back to top](#-table-of-contents)

---

### `needs_wrap_for_repeat`

A narrower hook than `_precedence`, added for one specific case: a multi-character
`Literal` quantified directly by `Repeat`. Regex quantifiers bind to exactly one
preceding token — never to more than one character of plain text — and `_precedence`
alone cannot express that narrower constraint (a `Literal` correctly needs no wrap
when embedded in a `Sequence`, but DOES need one when directly quantified).

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `bool`: `True` if this node, despite rendering at `ATOM` precedence (no wrap from
  the ordinary comparison), still needs an explicit `(?:...)` before a `Repeat`
  quantifier can apply to it as one unit. Defaults to `False` — every ATOM node
  except a multi-character `Literal` is already exactly one token.

**Example usage:**
```python
Repeat(Literal("ab"), min=3, max=3).to_pattern()   # -> "(?:ab){3}", not "ab{3}"
```

**Under the hood** *(the base default; `Literal` overrides)*:
```python
def needs_wrap_for_repeat(self) -> bool:
    return False
```

[▲ Back to top](#-table-of-contents)

---

### `to_char_class_fragment`

A rendering hook for use as a standalone item inside a `CharacterClass` (`[...]`),
where escaping rules genuinely differ from the rest of a pattern (e.g. `\1` outside a
class is a backreference, but inside one it's an octal escape — the two contexts can
give identical source text completely different meanings).

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `str`: This node's representation for use inside `[...]`. Defaults to
  `to_pattern()` — correct for any node whose escape syntax is genuinely identical
  either side of a class (`CharacterType`, `CharCode`). Only `Literal` overrides this
  (escaping just `] ^ - \`, a smaller set than the general-purpose `re.escape` it
  uses outside a class).

**Example usage:**
```python
CharacterClass(Literal("]"), Literal("^")).to_pattern()   # -> "[\]\^]"
```

Only ever called on nodes where `_usable_in_char_class` is `True` —
`CharacterClass.__init__` is responsible for that check; this method itself does not
re-validate it. See [`README_REGEX_ATOMS`](README_REGEX_ELEMENTS.md#characterclass) for
the full item-restriction mechanism.

[▲ Back to top](#-table-of-contents)

---

### `compile`

Convenience wrapper: compiles this node's own top-level pattern via `re.compile`
directly, for quick inspection/debugging without building a full `RegexPattern`.

**Parameters:**
* `flags` (*int*, default `0`): Passed straight through to `re.compile`.

**Returns:**
* `re.Pattern`: The compiled pattern object.

**Example usage:**
```python
DIGIT.compile().match("5")   # -> a re.Match object
```

Top-level rendering always uses `to_pattern()` directly — never `render()` — since
there is no parent context to wrap against at the root of a tree.

> 💡 For real, ongoing use (repeated `search`/`match`/`sub` calls, flag management via
> `Flag`), prefer [`RegexPattern`](README_REGEX_COMPILER.md) — this method exists for
> quick, one-off checks.

[▲ Back to top](#-table-of-contents)

---

### `__add__` / `__radd__`

Concatenates this node with another via `+` — the method behind `Sequence`
composition.

**Parameters:**
* `other` (*Regex*): The right-hand (or, via `__radd__`, left-hand) operand.

**Returns:**
* `Regex`: `Sequence(self, other)`, or `NotImplemented` if `other` isn't a `Regex`
  instance.

**Example usage:**
```python
greeting = Literal("hello") + Literal(" ") + Literal("world")
greeting.to_pattern()   # -> "hello\ world"
```

Deliberately NOT `&` — `Rule.__and__` means "both predicates must hold" (a genuine
boolean AND); two regex nodes placed next to each other don't "both have to hold" in
that sense, they concatenate. `+` reads correctly as "these go one after another."

[▲ Back to top](#-table-of-contents)

---

### `__or__` / `__ror__`

Combines this node with another via alternation — `node1 | node2` matches whichever
side matches. Equivalent to `Alternation(node1, node2)`.

**Parameters:**
* `other` (*Regex*): The right-hand (or, via `__ror__`, left-hand) operand.

**Returns:**
* `Regex`: `Alternation(self, other)`, or `NotImplemented` if `other` isn't a `Regex`
  instance.

**Example usage:**
```python
pet = Literal("cat") | Literal("dog")
pet.to_pattern()   # -> "cat|dog"
```

This is the one operator that keeps its meaning from `Rule`/`Action` — regex
alternation is a direct analogue of logical OR.

[▲ Back to top](#-table-of-contents)

---

## The `_Precedence` enum

Four binding-power levels, loosest to tightest, used exclusively by `render`:

| Level | Value | Example syntax |
|---|---|---|
| `ALTERNATION` | 0 | `A\|B` |
| `SEQUENCE` | 1 | `AB` |
| `REPEAT` | 2 | `A*`, `A{m,n}` |
| `ATOM` | 3 | a single char, `Group(...)`, `CharacterClass`, `Lookaround`, `Anchor`, ... |

A child is wrapped exactly when its own precedence is strictly lower than the level
its parent renders it at. `ATOM` is the ceiling — anything already self-delimiting
never needs an extra wrap, regardless of where it is embedded. Most nodes in the tree
stay at the base class's `ATOM` default and never override `_precedence` at all; only
`Sequence`, `Alternation`, and `Repeat` have a genuine precedence below `ATOM`.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-the-regex-class)
