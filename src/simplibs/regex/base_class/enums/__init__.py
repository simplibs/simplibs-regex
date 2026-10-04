from .Precedence import Precedence


_DESIGN_NOTES = """
# Regex Base Class Enums Sub-Package

## Purpose
The `enums` package provides internal enumerations used by the foundational 
abstract syntax tree (AST) building blocks and operator precedence rules.

## Internal Components Registry

| Component     | Type             | Description                                                                        |
| :------------ | :--------------- | :--------------------------------------------------------------------------------- |
| `Precedence`  | Internal Enum    | Precedence levels used to determine when parentheses are required during rendering.|
"""