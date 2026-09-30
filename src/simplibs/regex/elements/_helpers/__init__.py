from .char_class_escape import escape_char_class_char


_DESIGN_NOTES = """
# Regex Elements Helpers Sub-Package

## Purpose
Internal helper utilities specifically designed for regex elements and character class formatting.

## Internal Components Registry

| Component               | Type     | Description                                                                          |
| :---------------------- | :------- | :----------------------------------------------------------------------------------- |
| `escape_char_class_char`| Function | Escapes special characters exclusively needed inside character classes (`] ^ - \\`). |
"""