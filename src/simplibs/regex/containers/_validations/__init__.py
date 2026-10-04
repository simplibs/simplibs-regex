from .common import (
    raise_param_not_identifier_error,
    raise_no_nodes_error,
    raise_param_invalid_type_error,
)
from .conditional import (
    raise_conditional_invalid_numeric_id_error,
    raise_conditional_invalid_id_type_error,
)
from .group import (
    raise_group_atomic_and_flags_conflict_error,
    raise_group_atomic_and_name_conflict_error,
    raise_group_flags_off_without_flags_error,
    raise_group_flags_require_non_capturing_error,
    raise_group_name_and_flags_conflict_error,
    raise_group_name_requires_capturing_error,
    raise_flags_off_restricted_error,
    raise_locale_flag_unsupported_error,
    raise_group_flags_overlap_error,
    raise_group_ascii_unicode_conflict_error,
)
from .lookaround import raise_variable_length_lookbehind_error
from .repeat import (
    raise_repeat_inner_not_repeatable_error,
    raise_repeat_max_less_than_min_error,
    raise_repeat_min_negative_error,
)


_DESIGN_NOTES = """
# Containers Validations Sub-Package

## Purpose
Aggregates and exposes all structured exception emission helpers for regex containers validation.

## Internal Components Registry

| Component                                       | Type     | Description                                               |
| :---------------------------------------------- | :------- | :-------------------------------------------------------- |
| `raise_no_nodes_error`                          | Function | Containers requiring at least one node.        |
| `raise_param_invalid_type_error`                | Function | Parameter type validation.                     |
| `raise_param_not_identifier_error`              | Function | Parameter string identifier validation.        |
| `raise_conditional_invalid_numeric_id_error`    | Function | Conditional group numeric ID less than 1.                 |
| `raise_conditional_invalid_id_type_error`       | Function | Invalid conditional group ID/name data type.              |
| `raise_group_atomic_and_flags_conflict_error`   | Function | Conflict between atomic group and flags.                  |
| `raise_group_atomic_and_name_conflict_error`    | Function | Conflict between atomic group and name.                   |
| `raise_group_flags_off_without_flags_error`     | Function | Usage of `flags_off` without enabled `flags`.             |
| `raise_group_flags_require_non_capturing_error` | Function | Requirement for non-capturing state when setting flags.   |
| `raise_group_name_and_flags_conflict_error`     | Function | Conflict between group name and flags.                    |
| `raise_group_name_requires_capturing_error`     | Function | Named group requiring capturing.                          |
| `raise_flags_off_restricted_error`              | Function | Attempt to disable restricted flags (ASCII, UNICODE, LOCALE). |
| `raise_locale_flag_unsupported_error`           | Function | Usage of unsupported LOCALE flag.                         |
| `raise_group_flags_overlap_error`               | Function | Overlap of flags in both `flags` and `flags_off`.         |
| `raise_group_ascii_unicode_conflict_error`      | Function | Simultaneous conflict of ASCII and UNICODE flags.         |
| `raise_variable_length_lookbehind_error`        | Function | Variable length in lookbehind assertion.                  |
| `raise_repeat_inner_not_repeatable_error`       | Function | Repeat received a node that cannot be quantified directly.|
| `raise_repeat_max_less_than_min_error`          | Function | Upper repetition limit less than lower limit (`max < min`). |
| `raise_repeat_min_negative_error`               | Function | Negative minimum repetition count.                        |
"""