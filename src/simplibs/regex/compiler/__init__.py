from .RegexPattern import RegexPattern


_DESIGN_NOTES = """
# Regex Compiler Sub-Package

## Purpose
The `compiler` package provides the runtime compilation and execution layer for regex trees, 
acting as a convenient wrapper around Python's built-in `re.Pattern`.

## Internal Components Registry

| Component      | Type             | Description                                                                       |
| :------------- | :--------------- | :-------------------------------------------------------------------------------- |
| `RegexPattern` | Public Class     | Compiled, ready-to-use wrapper around a `Regex` tree providing search, match, etc.|
"""