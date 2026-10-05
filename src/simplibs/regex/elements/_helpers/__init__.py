from .char_class_escape import escape_char_class_char
from .escape_control_character import escape_control_character


_DESIGN_NOTES = """
# Regex Elements Helpers Sub-Package

## Purpose
Internal helper utilities specifically designed for regex elements and character class formatting.

## Internal Components Registry

| Component                 | Type     | Description                                                                          |
| :------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `escape_char_class_char`  | Function | Escapes special characters exclusively needed inside character classes (`] ^ - \\`). |
| `escape_control_character`| Function | Returns readable `re` escape for control characters (`\\t`, `\\n`, `\\xhh`), or None. |
"""