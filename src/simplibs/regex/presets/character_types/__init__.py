from .DIGIT import DIGIT
from .NON_DIGIT import NON_DIGIT
from .WORD_CHARACTER import WORD_CHARACTER
from .NON_WORD_CHARACTER import NON_WORD_CHARACTER
from .WHITESPACE import WHITESPACE
from .NON_WHITESPACE import NON_WHITESPACE


_DESIGN_NOTES = """
# Character Types Presets Sub-Package

## Purpose
Provides convenient character type presets (`DIGIT`, `WORD_CHARACTER`, `WHITESPACE`, and their negations) built on top of the underlying `CharacterType` element.

## Components Registry

| Component            | Type   | Description                                           |
| :------------------- | :----- | :---------------------------------------------------- |
| `DIGIT`              | Preset | Matches any decimal digit (`\\d`).                    |
| `NON_DIGIT`          | Preset | Matches any non-digit character (`\\D`).              |
| `WORD_CHARACTER`     | Preset | Matches any word character (`\\w`).                   |
| `NON_WORD_CHARACTER` | Preset | Matches any non-word character (`\\W`).               |
| `WHITESPACE`         | Preset | Matches any whitespace character (`\\s`).             |
| `NON_WHITESPACE`     | Preset | Matches any non-whitespace character (`\\S`).         |
"""