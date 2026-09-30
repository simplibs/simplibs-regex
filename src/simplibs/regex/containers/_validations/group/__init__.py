from .raise_group_atomic_and_flags_conflict_error import raise_group_atomic_and_flags_conflict_error
from .raise_group_atomic_and_name_conflict_error import raise_group_atomic_and_name_conflict_error
from .raise_group_flags_off_without_flags_error import raise_group_flags_off_without_flags_error
from .raise_group_flags_require_non_capturing_error import raise_group_flags_require_non_capturing_error
from .raise_group_inner_not_regex_error import raise_group_inner_not_regex_error
from .raise_group_name_and_flags_conflict_error import raise_group_name_and_flags_conflict_error
from .raise_group_name_requires_capturing_error import raise_group_name_requires_capturing_error
from .raise_invalid_group_name_error import raise_invalid_group_name_error

_DESIGN_NOTES = """
# Group Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Group container validation.

## Internal Components Registry

| Component                                       | Type     | Description                                                                     |
| :---------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_group_atomic_and_flags_conflict_error`   | Function | Emits structured `ParamError` on atomic and flags conflict.                    |
| `raise_group_atomic_and_name_conflict_error`    | Function | Emits structured `ParamError` on atomic and name conflict.                      |
| `raise_group_flags_off_without_flags_error`     | Function | Emits structured `ParamError` when flags_off is set without flags.              |
| `raise_group_flags_require_non_capturing_error` | Function | Emits structured `ParamError` when flags require non-capturing state.           |
| `raise_group_inner_not_regex_error`             | Function | Emits structured `ParamError` when group inner node is not a Regex.             |
| `raise_group_name_and_flags_conflict_error`     | Function | Emits structured `ParamError` on name and flags conflict.                       |
| `raise_group_name_requires_capturing_error`     | Function | Emits structured `ParamError` when group name requires capturing.               |
| `raise_invalid_group_name_error`                | Function | Emits structured `ParamError` when group name is invalid identifier.            |
"""