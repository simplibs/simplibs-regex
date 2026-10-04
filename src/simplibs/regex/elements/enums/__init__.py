from .AnchorKind import AnchorKind
from .CharacterTypeKind import CharacterTypeKind
from .CharacterCodeKind import CharacterCodeKind


_DESIGN_NOTES = """
# Elements Enums Sub-Package

## Purpose
The `enums` package provides internal and structural enumeration types 
used by regex element nodes to govern behavior and define syntax variants 
for anchors, character types, and character codes.

## Internal Components Registry

| Component           | Type   | Description                                                                     |
| :------------------ | :----- | :------------------------------------------------------------------------------ |
| `AnchorKind`        | Enum   | Specifies the type of zero-width position assertion (`^`, `$`, `\\b`, etc.). |
| `CharacterTypeKind` | Enum   | Specifies built-in Unicode character classes (`\\d`, `\\w`, `\\s`, etc.).    |
| `CharacterCodeKind` | Enum   | Specifies character-code escape syntaxes (`\\xFF`, `\\uFFFF`, etc.).          |
"""
