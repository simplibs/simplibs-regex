from .raise_group_reference_invalid_identifier_error import raise_group_reference_invalid_identifier_error
from .raise_group_reference_invalid_type_error import raise_group_reference_invalid_type_error
from .raise_group_reference_numeric_out_of_range_error import raise_group_reference_numeric_out_of_range_error

_DESIGN_NOTES = """
# GroupReference Validations Sub-Package

## Purpose
Provides structured exception emission helpers for GroupReference validation.

## Internal Components Registry

| Component                                             | Type     | Description                                                                     |
| :---------------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_group_reference_invalid_identifier_error`      | Function | Emits structured `ParamError` when a group reference name is not an identifier. |
| `raise_group_reference_invalid_type_error`            | Function | Emits structured `ParamError` when group reference receives an invalid type.    |
| `raise_group_reference_numeric_out_of_range_error`    | Function | Emits structured `ParamError` when numeric group id is less than 1.             |
"""