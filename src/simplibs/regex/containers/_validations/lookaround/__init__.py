from .raise_lookaround_inner_not_regex_error import raise_lookaround_inner_not_regex_error
from .raise_lookaround_invalid_direction_error import raise_lookaround_invalid_direction_error
from .raise_variable_length_lookbehind_error import raise_variable_length_lookbehind_error

_DESIGN_NOTES = """
# Lookaround Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Lookaround container validation.

## Internal Components Registry

| Component                                       | Type     | Description                                                                     |
| :---------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_lookaround_inner_not_regex_error`        | Function | Emits structured `ParamError` when lookaround inner node is not a Regex.        |
| `raise_lookaround_invalid_direction_error`      | Function | Emits structured `ParamError` when lookaround direction is invalid.             |
| `raise_variable_length_lookbehind_error`        | Function | Emits structured `ParamError` when lookbehind has variable length.              |
"""