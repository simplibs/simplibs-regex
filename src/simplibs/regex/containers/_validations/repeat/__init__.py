from .raise_repeat_inner_not_repeatable_error import raise_repeat_inner_not_repeatable_error
from .raise_repeat_max_less_than_min_error import raise_repeat_max_less_than_min_error
from .raise_repeat_min_negative_error import raise_repeat_min_negative_error

_DESIGN_NOTES = """
# Repeat Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Repeat container validation.

## Internal Components Registry

| Component                                 | Type     | Description                                                                     |
| :---------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_repeat_inner_not_repeatable_error` | Function | Emits structured `ParamError` when Repeat receives a node that cannot be repeated. |
| `raise_repeat_max_less_than_min_error`    | Function | Emits structured `ParamError` when max count is less than min count.            |
| `raise_repeat_min_negative_error`         | Function | Emits structured `ParamError` when minimum repetition count is negative.        |
"""