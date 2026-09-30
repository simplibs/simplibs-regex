# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
* `CharCode` / `CharCodeKind` — character-code escapes (`\xFF \uFFFF \Uhhhhhhhh
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