from .common import raise_param_invalid_type_error
from .anorch import raise_anchor_requires_python_314_error
from .character_code import (
    raise_character_code_invalid_kind_error,
    raise_character_code_invalid_named_value_error,
    raise_character_code_invalid_type_error,
    raise_character_code_out_of_range_error,
    raise_character_code_unknown_name_error,
)
from .character_class import (
    raise_character_class_empty_error,
    raise_character_class_item_not_allowed_error,
    raise_multi_character_literal_in_char_class_error,
)
from .character_range import (
    raise_character_range_invalid_boundary_error,
    raise_character_range_start_after_end_error,
    raise_character_range_no_standalone_pattern_error,
)
from .group_reference import (
    raise_group_reference_invalid_identifier_error,
    raise_group_reference_invalid_type_error,
    raise_group_reference_numeric_out_of_range_error,
)
from .literal import (
    raise_literal_empty_error,
    raise_literal_not_single_char_error,
)
from .raw_pattern import raise_raw_pattern_empty_error

_DESIGN_NOTES = """
# Atoms Validations Sub-Package

## Purpose
Aggregates and exposes all structured exception emission helpers for regex atoms and containers validation.

## Internal Components Registry

| Component                                           | Type     | Description                                       |
| :-------------------------------------------------- | :------- | :------------------------------------------------ |
| `raise_param_invalid_type_error`                    | Function | Parameter type validation helper.       |
| `raise_anchor_requires_python_314_error`            | Function | Anchor Python 3.14 support validation.  |
| `raise_character_code_invalid_kind_error`           | Function | CharacterCode kind validation helper.   |
| `raise_character_code_invalid_named_value_error`    | Function | CharacterCode named value validation helper. |
| `raise_character_code_invalid_type_error`           | Function | CharacterCode type validation helper.   |
| `raise_character_code_out_of_range_error`           | Function | CharacterCode range validation helper.  |
| `raise_character_code_unknown_name_error`           | Function | CharacterCode unknown name validation helper.     |
| `raise_character_class_empty_error`                 | Function | CharacterClass empty validation helper. |
| `raise_character_class_item_not_allowed_error`      | Function | CharacterClass item restriction helper. |
| `raise_multi_character_literal_in_char_class_error` | Function | Multi-character literal check helper.   |
| `raise_character_range_invalid_boundary_error`      | Function | CharacterRange boundary validation helper. |
| `raise_character_range_start_after_end_error`       | Function | CharacterRange order validation helper. |
| `raise_character_range_no_standalone_pattern_error` | Function | CharacterRange is rendered standalone.  |   
| `raise_group_reference_invalid_identifier_error`    | Function | GroupReference identifier validation helper. |
| `raise_group_reference_invalid_type_error`          | Function | GroupReference type validation helper. |
| `raise_group_reference_numeric_out_of_range_error`  | Function | GroupReference numeric range validation helper. |
| `raise_literal_empty_error`                         | Function | Literal empty validation helper.        |
| `raise_literal_not_single_char_error`               | Function | Literal single-character check helper.  |
| `raise_raw_pattern_empty_error`                     | Function | RawPattern empty text validation helper. |
"""