from .ANY import ANY


_DESIGN_NOTES = """
# Any Character Presets Sub-Package

## Purpose
Provides the `ANY` preset, a shared instance of `AnyCharacter` (the `.` wildcard).

## Components Registry

| Component | Type   | Built on       | Description                                  |
| :-------- | :----- | :------------- | :------------------------------------------- |
| `ANY`     | Preset | `AnyCharacter` | Matches any single character (`.`).          |

## Why it is not in `character_types`
`ANY` is not a `CharacterType`: unlike `DIGIT`, `WORD_CHARACTER` and the others it
cannot be used inside a `CharacterClass` (`[.]` is a literal dot), so it
lives in its own sub-package.
"""