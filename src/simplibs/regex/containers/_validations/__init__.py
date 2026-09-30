from .alternation_and_sequence import (
    raise_node_param_not_regex_error,
    raise_requires_at_least_one_node_error,
)
from .conditional import (
    raise_conditional_invalid_id_type_error,
    raise_conditional_invalid_name_error,
    raise_conditional_invalid_numeric_id_error,
    raise_conditional_no_not_regex_error,
    raise_conditional_yes_not_regex_error,
)
from .group import (
    raise_group_atomic_and_flags_conflict_error,
    raise_group_atomic_and_name_conflict_error,
    raise_group_flags_off_without_flags_error,
    raise_group_flags_require_non_capturing_error,
    raise_group_inner_not_regex_error,
    raise_group_name_and_flags_conflict_error,
    raise_group_name_requires_capturing_error,
    raise_invalid_group_name_error,
)
from .lookaround import (
    raise_lookaround_inner_not_regex_error,
    raise_lookaround_invalid_direction_error,
    raise_variable_length_lookbehind_error,
)
from .repeat import (
    raise_repeat_inner_not_regex_error,
    raise_repeat_invalid_mode_error,
    raise_repeat_max_less_than_min_error,
    raise_repeat_min_negative_error,
)

_DESIGN_NOTES = """
# Containers Validations Sub-Package

## Purpose
Aggregates and exposes all structured exception emission helpers for regex containers validation.

## Internal Components Registry

| Component                                       | Type     | Description                                      |
| :---------------------------------------------- | :------- | :----------------------------------------------- |
| `raise_node_param_not_regex_error`              | Function | Sequence/Alternation node type validation.       |
| `raise_requires_at_least_one_node_error`        | Function | Sequence/Alternation empty nodes check.          |
| `raise_conditional_invalid_id_type_error`       | Function | Conditional ID type validation.                  |
| `raise_conditional_invalid_name_error`          | Function | Conditional group name validation.               |
| `raise_conditional_invalid_numeric_id_error`    | Function | Conditional numeric ID validation.               |
| `raise_conditional_no_not_regex_error`          | Function | Conditional negative branch validation.          |
| `raise_conditional_yes_not_regex_error`         | Function | Conditional positive branch validation.          |
| `raise_group_atomic_and_flags_conflict_error`   | Function | Group atomic & flags conflict check.             |
| `raise_group_atomic_and_name_conflict_error`    | Function | Group atomic & name conflict check.              |
| `raise_group_conflict_error`                    | Function | Group general option conflict check.             |
| `raise_group_flags_off_without_flags_error`     | Function | Group flags_off usage validation.                |
| `raise_group_flags_require_non_capturing_error` | Function | Group flags non-capturing requirement check.     |
| `raise_group_inner_not_regex_error`             | Function | Group inner node validation.                     |
| `raise_group_name_and_flags_conflict_error`     | Function | Group name & flags conflict check.               |
| `raise_group_name_requires_capturing_error`     | Function | Group name capturing requirement check.          |
| `raise_invalid_group_name_error`                | Function | Group name identifier validation.                |
| `raise_lookaround_inner_not_regex_error`        | Function | Lookaround inner node validation.                |
| `raise_lookaround_invalid_direction_error`      | Function | Lookaround direction validation.                 |
| `raise_variable_length_lookbehind_error`        | Function | Lookbehind variable length validation.           |
| `raise_repeat_inner_not_regex_error`            | Function | Repeat inner node validation.                    |
| `raise_repeat_invalid_mode_error`               | Function | Repeat mode validation.                          |
| `raise_repeat_max_less_than_min_error`          | Function | Repeat range bounds check (max < min).           |
| `raise_repeat_min_negative_error`               | Function | Repeat minimum negative check.                   |
"""