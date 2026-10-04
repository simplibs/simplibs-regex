from .raise_param_invalid_type_error import raise_param_invalid_type_error

_DESIGN_NOTES = """
# Common Element Validations Sub-Package

## Purpose
Provides shared helper functions for validating general parameters in elements.

## Internal Components Registry

| Component                          | Type     | Description                                                                     |
| :--------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_param_invalid_type_error`   | Function | Raises a ParamError if an element parameter has the wrong type.                |
"""