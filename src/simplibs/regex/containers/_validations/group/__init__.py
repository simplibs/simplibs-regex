from .raise_group_atomic_and_flags_conflict_error import raise_group_atomic_and_flags_conflict_error
from .raise_group_atomic_and_name_conflict_error import raise_group_atomic_and_name_conflict_error
from .raise_group_flags_off_without_flags_error import raise_group_flags_off_without_flags_error
from .raise_group_flags_require_non_capturing_error import raise_group_flags_require_non_capturing_error
from .raise_group_name_and_flags_conflict_error import raise_group_name_and_flags_conflict_error
from .raise_group_name_requires_capturing_error import raise_group_name_requires_capturing_error
from .raise_flags_off_restricted_error import raise_flags_off_restricted_error
from .raise_locale_flag_unsupported_error import raise_locale_flag_unsupported_error
from .raise_group_flags_overlap_error import raise_group_flags_overlap_error
from .raise_group_ascii_unicode_conflict_error import raise_group_ascii_unicode_conflict_error


_DESIGN_NOTES = """
# Group Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Group container validation.

## Internal Components Registry

| Component                                       | Type     | Description                                                                     |
| :---------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_group_atomic_and_flags_conflict_error`   | Function | Emits structured `ParamError` on atomic and flags conflict.                     |
| `raise_group_atomic_and_name_conflict_error`    | Function | Emits structured `ParamError` on atomic and name conflict.                      |
| `raise_group_flags_off_without_flags_error`     | Function | Emits structured `ParamError` when flags_off is set without flags.              |
| `raise_group_flags_require_non_capturing_error` | Function | Emits structured `ParamError` when flags require non-capturing state.           |
| `raise_group_name_and_flags_conflict_error`     | Function | Emits structured `ParamError` on name and flags conflict.                       |
| `raise_group_name_requires_capturing_error`     | Function | Emits structured `ParamError` when group name requires capturing.               |
| `raise_flags_off_restricted_error`              | Function | Emits structured `ValidationError` when restricted flags are turned off.        |
| `raise_locale_flag_unsupported_error`           | Function | Emits structured `ValidationError` when Flag.LOCALE is used.                    |
| `raise_group_flags_overlap_error`               | Function | Emits structured `ValidationError` on overlapping flags and flags_off.          |
| `raise_group_ascii_unicode_conflict_error`      | Function | Emits structured `ValidationError` on ASCII and UNICODE conflict.               |
"""