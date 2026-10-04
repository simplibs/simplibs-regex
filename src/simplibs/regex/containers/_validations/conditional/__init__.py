from .raise_conditional_invalid_id_type_error import raise_conditional_invalid_id_type_error
from .raise_conditional_invalid_numeric_id_error import raise_conditional_invalid_numeric_id_error


_DESIGN_NOTES = """
# Conditional Validations Sub-Package

## Purpose
Provides specialized functions for validating group identifiers and their types in conditional expressions (Conditional).

## Internal Components Registry

| Component                                  | Type     | Description                                                                     |
| :----------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_conditional_invalid_id_type_error`  | Function | Raises a ParamError upon an invalid group ID/name data type (e.g., boolean).    |
| `raise_conditional_invalid_numeric_id_error`| Function | Raises a ParamError if the numeric group ID is less than 1.                     |
"""