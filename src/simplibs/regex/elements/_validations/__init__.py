from .anorch import raise_anchor_invalid_kind_error
from .char_code import (
    raise_char_code_invalid_kind_error,
    raise_char_code_invalid_named_value_error,
    raise_char_code_invalid_type_error,
    raise_char_code_out_of_range_error,
)
from .character_class import (
    raise_char_class_empty_error,
    raise_char_class_item_not_allowed_error,
    raise_multi_char_literal_in_char_class_error,
)
from .character_range import (
    raise_character_range_invalid_boundary_error,
    raise_character_range_no_standalone_pattern_error,
    raise_character_range_start_after_end_error,
)
from .character_type import raise_character_type_invalid_kind_error
from .group_reference import (
    raise_group_reference_invalid_identifier_error,
    raise_group_reference_invalid_type_error,
    raise_group_reference_numeric_out_of_range_error,
)
from .literal import (
    raise_literal_empty_error,
    raise_literal_invalid_type_error,
    raise_literal_not_single_char_error,
)

_DESIGN_NOTES = """
# Atoms Validations Sub-Package

## Purpose
Aggregates and exposes all structured exception emission helpers for regex atoms and containers validation.

## Internal Components Registry

| Component                                            | Type     | Description                                      |
| :--------------------------------------------------- | :------- | :----------------------------------------------- |
| `raise_anchor_invalid_kind_error`                    | Function | Anchor validation helper.                        |
| `raise_char_code_invalid_kind_error`                 | Function | CharCode kind validation helper.                 |
| `raise_char_code_invalid_named_value_error`          | Function | CharCode named value validation helper.          |
| `raise_char_code_invalid_type_error`                 | Function | CharCode type validation helper.                 |
| `raise_char_code_out_of_range_error`                 | Function | CharCode range validation helper.                |
| `raise_char_class_empty_error`                       | Function | CharacterClass empty validation helper.          |
| `raise_char_class_item_not_allowed_error`            | Function | CharacterClass item restriction helper.          |
| `raise_multi_char_literal_in_char_class_error`       | Function | Multi-character literal check helper.            |
| `raise_character_range_invalid_boundary_error`       | Function | CharacterRange boundary validation helper.       |
| `raise_character_range_no_standalone_pattern_error`  | Function | CharacterRange standalone pattern check helper.  |
| `raise_character_range_start_after_end_error`        | Function | CharacterRange order validation helper.          |
| `raise_character_type_invalid_kind_error`            | Function | CharacterType kind validation helper.            |
| `raise_group_reference_invalid_identifier_error`     | Function | GroupReference identifier validation helper.     |
| `raise_group_reference_invalid_type_error`           | Function | GroupReference type validation helper.           |
| `raise_group_reference_numeric_out_of_range_error`   | Function | GroupReference numeric range validation helper.  |
| `raise_literal_empty_error`                          | Function | Literal empty validation helper.                 |
| `raise_literal_invalid_type_error`                   | Function | Literal type validation helper.                  |
| `raise_literal_not_single_char_error`                | Function | Literal single-character check helper.           |
"""