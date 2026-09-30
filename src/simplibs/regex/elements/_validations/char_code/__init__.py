from .raise_char_code_invalid_kind_error import raise_char_code_invalid_kind_error
from .raise_char_code_invalid_named_value_error import raise_char_code_invalid_named_value_error
from .raise_char_code_invalid_type_error import raise_char_code_invalid_type_error
from .raise_char_code_out_of_range_error import raise_char_code_out_of_range_error

_DESIGN_NOTES = """
# CharCode Validations Sub-Package

## Purpose
Provides structured exception emission helpers for CharCode validation.

## Internal Components Registry

| Component                                     | Type     | Description                                                                     |
| :-------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_char_code_invalid_kind_error`          | Function | Emits structured `ParamError` when an invalid CharCodeKind is received.         |
| `raise_char_code_invalid_named_value_error`   | Function | Emits structured `ParamError` when a named CharCode receives an invalid value.  |
| `raise_char_code_invalid_type_error`          | Function | Emits structured `ParamError` when a numeric CharCode receives a non-int type.  |
| `raise_char_code_out_of_range_error`          | Function | Emits structured `ParamError` when a numeric CharCode value is out of range.    |
"""