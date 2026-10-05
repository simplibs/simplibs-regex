# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.3.0] - 2026-10-05

### ✨ Added

#### Testing

* `assert_pattern(finds=...)` — context checks for terms that depend on their surroundings
  (lookarounds): maps a text to the substring a `search` in it must return, or to `None`
  when nothing may be found. `fullmatch`, used by `matches` / `non_matches`, cannot express
  this (`(?<=key=).+` never fully matches `"value"`).

#### Documentation

* `finds` documented in `docs/README_REGEX_TESTING.md` (new "Context checks" section) and
  mentioned in the root `README.md`

### 🔄 Changed

* `Literal`, `CharacterRange` and character classes — control characters are rendered as
  readable escapes (`\t \n \r \f \v \a`, other controls `\xhh`) instead of a backslash plus the
  invisible character (`re.escape`'s output) or, inside `[...]`, the raw character. The pattern
  string changes (`Literal("\n").to_pattern()` is now `\n`), the matching does not. A space stays
  `\ `. The `TAB`, `NEWLINE`, `CARRIAGE_RETURN`, `FORM_FEED`, `VERTICAL_TAB` and `BELL` presets
  render accordingly.

### 📋 Improved

* `assert_pattern` — failure messages show the expected / actual pattern strings with
  `repr`; patterns with real control characters (e.g. a verbatim `RawPattern("a\nb")`) no
  longer break the message across lines

---

## [0.2.0] - 2026-10-02

### ✨ Added

#### Core Class

* `Regex._repeatable` — class-level marker (default `True`) for nodes `re` refuses to quantify
  directly; `Anchor` sets it to `False`. `Repeat` reads it at construction time.

#### Containers

* `Repeat` rejects a bare `Anchor` as `inner` at construction time (`^*`, `\b?`, `\A?` fail in `re`
  with "nothing to repeat"); an anchor wrapped in a `Group`, or a lookaround, stays legal

#### Elements

* `AnyCharacter` — the `.` wildcard node. Never usable inside a `CharacterClass`
  (`[.]` means a literal dot), enforced at construction time. It was listed in 0.1.0
  but missing from the package.
* `CharacterRange.__repr__` — `CharacterRange('a', 'z')`; the inherited `repr` is built
  from `to_pattern()`, which deliberately raises for a bare range

#### Presets

* `any_character` — `ANY`, the shared `AnyCharacter` instance
* `character_classes`, `literals` and the `WITH_FLAGS`, `CASE_INSENSITIVE`, `VERBOSE_GROUP` group presets —
  listed in 0.1.0 but missing from the package

#### Testing

* `testing` — new sub-package with the `assert_pattern` test helper: verifies a
  term's rendered pattern string and its matching / non-matching texts, with isolated
  subtests (`verbose=True`) or fail-fast behaviour (`verbose=False`), compiled through
  `RegexPattern` with optional `flags`. Available as `simplibs.regex.testing`; it is
  deliberately not re-exported from the top-level `simplibs.regex` package.

#### Documentation

* `docs/README_REGEX_TESTING.md` and a `testing/` section in the root `README.md`
* `compiled` property documented in `docs/README_REGEX_COMPILER.md`
* Requirements section in the root `README.md`

### 🐛 Fixed

* `Repeat` — a nested `Repeat` is now wrapped: `Repeat(Repeat(x), min=3, max=3)`
  rendered `x*{3}`, which `re` rejects ("multiple repeat"); it now renders `(?:x*){3}`.
  The inner node is rendered at `ATOM` precedence.
* `Conditional` — a `Sequence` or `Alternation` branch is now wrapped in `(?:...)`.
  An unwrapped alternation added extra branches to `(?(1)yes|no)` (`re` accepts exactly
  two) or silently shifted the yes/no split.
* `Group` — the same flag in both `flags` and `flags_off`, and `ASCII` together with `UNICODE`, are now
  rejected at construction time (`re.compile` rejects both)
* `Group` — `flags_off` together with an explicit empty `flags=frozenset()` was
  rejected, although the error message itself recommended that form
* `CharacterClass` / `Literal` — `[ & ~ |` are now escaped inside `[...]`; adjacent
  single-character literals could form `[[`, `&&`, `||`, `~~`, which `re` reserves for
  future set operations and flags with a `FutureWarning`
* `RegexPattern` — incompatible top-level flags (`ASCII` together with `UNICODE`) leaked
  a bare `ValueError` from `re.compile`; it is now reported as the structured
  invalid-pattern error like every other compile failure
* `CharacterCode` — the upper bound of octal escapes is now `0o377` (was `0o777`);
  `\400` and above are rejected by Python's `re`, and are now rejected at construction
  time instead of failing later in `re.compile()`
* `CharacterCode` — `bool` values are rejected instead of silently rendering as `\x01`
* `CharacterCode` — an unknown Unicode name (or the name of a multi-character named sequence) for
  `NAMED` is rejected at construction time instead of when the pattern is compiled
* `GroupReference` — numeric ids are limited to `1`–`99` (`\100` and above are octal
  escapes in Python's `re`); `bool` values are rejected

### 🔄 Changed

* `GroupReference` — a numeric reference embedded in a `Sequence` or `Repeat` now
  renders wrapped, `(?:\1)`, so a following digit can no longer merge into its number
  (`\1` + `0` used to render `\10`). Standalone rendering is unchanged (`\1`).
* Type-check errors — every wrong-typed constructor argument is now reported by one shared helper,
  `raise_param_invalid_type_error` (`PARAM_INVALID_TYPE_ERROR`, a `ParamError` wrapping `TypeError`),
  instead of one dedicated `raise_*` function per parameter; the message names the parameter,
  the expected type and an example
* `Group`, `RegexPattern` and `assert_pattern` — `flags` (and `flags_off`) accept any `set` or `frozenset` of
  `Flag`; `Group` and `RegexPattern` store it as a `frozenset`
* Internal layout — `_Precedence` is now `Precedence` in `base_class/enums/`, and the
  kind enums (`AnchorKind`, `CharacterTypeKind`, `CharacterCodeKind`, `RepeatMode`,
  `LookaroundDirection`) live in `enums/` sub-packages of their package
* `Regex.compile` — return annotation is `re.Pattern[str]` (was `Any`)

### 📋 Improved

* Documentation corrected against the code: stale `_Precedence` / `atoms/` references,
  broken cross-README anchors, wrong example results (`findall`, `sub`,
  `pattern_string`), the flag-restriction and `Conditional` / `Repeat` wrapping rules,
  and Unicode behaviour of the `character_types` presets
* Preset docstrings: `DIGIT` / `WORD` are Unicode-aware, `WORD_BOUNDARY` and `END`
  described precisely

### 📦 Requirements

* Python 3.11+
* simple-exception 1.0.0+

---

## [0.1.0] - 2026-09-30

### ✨ Added

#### Core Class

* `Regex` — abstract base class every node in the library inherits from, defining the
  mandatory `to_pattern` contract plus precedence-aware rendering (`render`),
  fixed-length introspection (`fixed_length`), the `needs_wrap_for_repeat` and
  `to_char_class_fragment` rendering hooks, and `+`/`\|` operator composition
  (`Sequence`/`Alternation`)
* `_Precedence` — the four-level binding-power enum (`ALTERNATION` < `SEQUENCE` <
  `REPEAT` < `ATOM`) `render` uses to decide when a child node needs wrapping in
  `(?:...)`

#### Containers

* `Sequence` — concatenation, self-flattening, behind `+`
* `Alternation` — logical OR, self-flattening, behind `\|`
* `Repeat` / `RepeatMode` — unifies all 14 Python `re` quantifier syntaxes (`*` `+`
  `?` `{n}` `{n,}` `{m,n}` × greedy/lazy/possessive) into one `min`/`max`/`mode`
  mechanism
* `Group` — unifies all 6 group syntaxes (`()`, `(?:)`, `(?P<name>)`, `(?>)`,
  `(?flags:)`, `(?flags-flags:)`) into one `capturing`/`name`/`atomic`/`flags`/
  `flags_off` mechanism, with construction-time validation of flag-combination
  restrictions Python's `re` actually enforces
* `Lookaround` / `LookaroundDirection` — unifies all 4 lookaround syntaxes into one
  `direction`/`negate` mechanism, rejecting a variable-length lookbehind at
  construction time via `fixed_length`
* `Conditional` — group-existence branching (`(?(id/name)yes\|no)`)

#### Elements

* `Literal` — literal text, auto-escaped via `re.escape`, with a dedicated
  character-class-safe escaping path
* `RawPattern` - escape hatch for raw regex syntax with no dedicated node yet.
* `Anchor` / `AnchorKind` — zero-width position assertions (`^ $ \A \Z \b \B`), plus
  `END_STRING_PY314` (`\z`) guarded at construction time for interpreters below
  Python 3.14
* `AnyCharacter` — the `.` wildcard, exposed as a stateless singleton preset
* `CharacterType` / `CharacterTypeKind` — built-in classes (`\d \D \w \W \s \S`)
* `CharacterRange` — `a-z`-style ranges, valid only inside `CharacterClass`
* `CharacterClass` — `[...]` / `[^...]`, enforcing at construction time that every
  item is legal in character-class context (different escaping/meaning rules apply
  inside `[...]` than outside it)
* `GroupReference` — backreferences (`\1` … `\99`, `(?P=name)`)
* `CharacterCode` / `CharacterCodeKind` — character-code escapes (`\xFF \uFFFF \Uhhhhhhhh
  \N{name} \ooo`), with per-kind numeric range validation

#### Flags

* `Flag` — the seven inline/compile-time regex flags (`ASCII`, `IGNORECASE`,
  `LOCALE`, `MULTILINE`, `DOTALL`, `UNICODE`, `VERBOSE`), with `LOCALE` rejected
  outright (unusable with `str` patterns) and `flags_off` restricted to the four
  flags Python's `re` actually allows to be turned off

#### Compiler

* `RegexPattern` — compiled, ready-to-use runtime wrapper around a `Regex` tree,
  exposing `search`/`match`/`fullmatch`/`findall`/`finditer`/`sub`/`subn`/`split` as
  thin delegation to the underlying `re.Pattern`, compiled once at construction

#### Presets

* `anchors` — `START`, `END`, `START_STRING`, `END_STRING`, `WORD_BOUNDARY`,
  `NON_WORD_BOUNDARY`
* `any_character` — `ANY`
* `character_types` — `DIGIT`, `NON_DIGIT`, `WORD`, `NON_WORD`, `WHITESPACE`,
  `NON_WHITESPACE`
* `character_classes` — `LOWERCASE_LETTER`, `UPPERCASE_LETTER`, `LETTER`,
  `ALPHANUMERIC`, `HEX_DIGIT`
* `literals` — `TAB`, `NEWLINE`, `CARRIAGE_RETURN`, `FORM_FEED`, `VERTICAL_TAB`,
  `BELL`, `BACKSLASH_CHAR`
* `quantifiers` — `OPTIONAL`, `ZERO_OR_MORE`, `ONE_OR_MORE`, `EXACTLY`, `AT_LEAST`,
  `BETWEEN`
* `groups` — `NAMED_GROUP`, `NON_CAPTURING`, `ATOMIC_GROUP`, `WITH_FLAGS`,
  `CASE_INSENSITIVE`, `VERBOSE_GROUP`
* `lookaround` — `LOOKAHEAD`, `NEGATIVE_LOOKAHEAD`, `LOOKBEHIND`,
  `NEGATIVE_LOOKBEHIND`

#### Documentation

* Root `README.md` — quick start and full package-structure overview, shared across
  GitHub and PyPI
* Full method-by-method reference documentation for `Regex`, every container, and
  `RegexPattern`
* Complete card-per-construct reference documentation for every atom, flag, and
  preset

#### Quality Assurance

* Test suite covering every node's `to_pattern`/`fixed_length` output, precedence
  wrapping, construction-time validation (flag-combination restrictions, variable
  length lookbehind rejection, character-class item legality, numeric range checks),
  and end-to-end compilation against Python's own `re.compile`

#### Requirements

* Python 3.11+
* simple-exception 1.0.0+

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)