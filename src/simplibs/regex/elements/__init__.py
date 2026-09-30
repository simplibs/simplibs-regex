from .Anchor import Anchor
from .CharacterClass import CharacterClass
from .CharacterRange import CharacterRange
from .CharacterType import CharacterType
from .CharCode import CharCode
from .GroupReference import GroupReference
from .Literal import Literal
from .RawPattern import RawPattern
from .enums import AnchorKind, CharacterTypeKind, CharCodeKind


_DESIGN_NOTES = """
# Regex Elements Sub-Package

## Purpose
The `elements` package provides foundational atomic AST node building blocks for the regex library, 
including literals, anchors, character classes, character types, references, and their corresponding enums.

## Internal Components Registry

| Component           | Type            | Description                                                                     |
| :------------------ | :-------------- | :------------------------------------------------------------------------------ |
| `Anchor`            | Element Class   | Zero-width position assertions (`^`, `$`, `\\A`, `\\b`, etc.).                  |
| `AnchorKind`        | Enum            | Specifies the type of zero-width position assertion.                            |
| `CharacterClass`    | Element Class   | Sets of alternative characters or negation (`[...]`).                           |
| `CharacterRange`    | Element Class   | Contiguous character ranges for character classes (`a-z`).                      |
| `CharacterType`     | Element Class   | Built-in character classes like digits or whitespace (`\\d`, `\\w`, `\\s`).     |
| `CharacterTypeKind` | Enum            | Specifies built-in Unicode character classes.                                   |
| `CharCode`          | Element Class   | Specific character codes via hex, unicode, octal, or name (`\\x41`, `\\N{...}`).|
| `CharCodeKind`      | Enum            | Specifies character-code escape syntaxes.                                       |
| `GroupReference`    | Element Class   | Backreferences to previously captured groups (`\\1`, `(?P=name)`).              |
| `Literal`           | Element Class   | Exact literal text matching with automatic special character escaping.          |
| `RawPattern`        | Element Class   | Escape hatch for raw, unescaped regex syntax inserted verbatim.                 |
"""
