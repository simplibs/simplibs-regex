from .enums import Precedence
from .Regex import Regex


_DESIGN_NOTES = """
# Regex Base Class Sub-Package

## Purpose
The `base_class` package provides the foundational abstract syntax tree (AST) building blocks 
for the regex library, including operator overloading, precedence levels, and fragment generation hooks.

## Internal Components Registry

| Component     | Type             | Description                                                                        |
| :------------ | :--------------- | :--------------------------------------------------------------------------------- |
| `Regex`       | Abstract Class   | The root abstract class for all regex AST nodes, defining operators and hooks.     |
| `Precedence` | Internal Enum    | Precedence levels used to determine when parentheses are required during rendering.|
"""