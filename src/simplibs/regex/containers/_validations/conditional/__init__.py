from .raise_conditional_invalid_id_type_error import raise_conditional_invalid_id_type_error
from .raise_conditional_invalid_name_error import raise_conditional_invalid_name_error
from .raise_conditional_invalid_numeric_id_error import raise_conditional_invalid_numeric_id_error
from .raise_conditional_no_not_regex_error import raise_conditional_no_not_regex_error
from .raise_conditional_yes_not_regex_error import raise_conditional_yes_not_regex_error

_DESIGN_NOTES = """
# Conditional Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Conditional container validation.

## Internal Components Registry

| Component                                     | Type     | Description                                                                     |
| :-------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_conditional_invalid_id_type_error`     | Function | Emits structured `ParamError` when conditional id has an invalid type.          |
| `raise_conditional_invalid_name_error`        | Function | Emits structured `ParamError` when conditional group name is invalid.           |
| `raise_conditional_invalid_numeric_id_error`  | Function | Emits structured `ParamError` when conditional numeric id is out of range.      |
| `raise_conditional_no_not_regex_error`        | Function | Emits structured `ParamError` when alternative branch (no) is not a Regex.      |
| `raise_conditional_yes_not_regex_error`       | Function | Emits structured `ParamError` when primary branch (yes) is not a Regex.         |
"""