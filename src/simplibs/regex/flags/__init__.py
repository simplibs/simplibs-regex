from .Flag import Flag


_DESIGN_NOTES = """
# Regex Flags Sub-Package

## Purpose
The `flags` package provides inline and top-level compilation flags for regular expressions, 
mapping human-readable constants to Python's built-in `re` module flags.

## Internal Components Registry

| Component  | Type  | Description                                                                    |
|:-----------|:------|:-------------------------------------------------------------------------------|
| `Flag`     | Enum  | Inline and compilation regex flags (`ASCII`, `IGNORECASE`, `MULTILINE`, etc.). |
"""