_DESIGN_NOTES = """
# Regex Presets Sub-Package

## Purpose
The `presets` package provides a rich vocabulary of ready-to-use syntactic shortcuts, 
helpers, and atomic aliases (anchors, the `.` wildcard, character types and classes, 
literals, groups, lookarounds, and quantifiers) that make constructing expressions 
using the regex DSL clean and intuitive.

## Sub-Package Registry

| Sub-Package         | Description                                                                     |
| :------------------ | :------------------------------------------------------------------------------ |
| `anchors`           | Zero-width position assertions (`START`, `END`, `WORD_BOUNDARY`, etc.).         |
| `any_character`     | The `.` wildcard shorthand (`ANY`).                                             |
| `character_classes` | Common `[...]` compositions (`LETTER`, `ALPHANUMERIC`, `HEX_DIGIT`, etc.).      |
| `character_types`   | Built-in character class shorthands (`DIGIT`, `WORD_CHARACTER`, `WHITESPACE`, etc.).      |
| `groups`            | Capturing, non-capturing, named, and atomic grouping helpers.                   |
| `literals`          | Control-character literals (`TAB`, `NEWLINE`, `BACKSLASH`, etc.).          |
| `lookaround`        | Positive and negative lookahead/lookbehind assertions.                          |
| `quantifiers`       | Repeat wrappers like `OPTIONAL`, `ZERO_OR_MORE`, `BETWEEN`, etc.                |
"""