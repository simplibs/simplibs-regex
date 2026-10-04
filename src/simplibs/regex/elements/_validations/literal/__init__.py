from .raise_literal_empty_error import raise_literal_empty_error
from .raise_literal_not_single_char_error import raise_literal_not_single_char_error

_DESIGN_NOTES = """
# Literal Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Literal validation.

## Internal Components Registry

| Component                               | Type     | Description                                                                     |
| :-------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_literal_empty_error`             | Function | Emits structured `ParamError` when Literal receives an empty string.            |
| `raise_literal_not_single_char_error`   | Function | Emits structured `ParamError` when a multi-character Literal is used as fragment.|
"""