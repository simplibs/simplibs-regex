from .raise_repeat_inner_not_regex_error import raise_repeat_inner_not_regex_error
from .raise_repeat_invalid_mode_error import raise_repeat_invalid_mode_error
from .raise_repeat_max_less_than_min_error import raise_repeat_max_less_than_min_error
from .raise_repeat_min_negative_error import raise_repeat_min_negative_error

_DESIGN_NOTES = """
# Repeat Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Repeat container validation.

## Internal Components Registry

| Component                                 | Type     | Description                                                                     |
| :---------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_repeat_inner_not_regex_error`      | Function | Emits structured `ParamError` when repeat inner node is not a Regex.            |
| `raise_repeat_invalid_mode_error`         | Function | Emits structured `ParamError` when repeat mode is invalid.                      |
| `raise_repeat_max_less_than_min_error`    | Function | Emits structured `ParamError` when max count is less than min count.            |
| `raise_repeat_min_negative_error`         | Function | Emits structured `ParamError` when minimum repetition count is negative.        |
"""