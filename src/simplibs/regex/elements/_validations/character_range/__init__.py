from .raise_character_range_invalid_boundary_error import raise_character_range_invalid_boundary_error
from .raise_character_range_no_standalone_pattern_error import raise_character_range_no_standalone_pattern_error
from .raise_character_range_start_after_end_error import raise_character_range_start_after_end_error

_DESIGN_NOTES = """
# CharacterRange Validations Sub-Package

## Purpose
Provides structured exception emission helpers for CharacterRange validation.

## Internal Components Registry

| Component                                            | Type     | Description                                                                     |
| :--------------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_character_range_invalid_boundary_error`       | Function | Emits structured `ParamError` when a range boundary is not a single character.  |
| `raise_character_range_no_standalone_pattern_error`  | Function | Emits structured `ParamError` when to_pattern() is called on CharacterRange.    |
| `raise_character_range_start_after_end_error`        | Function | Emits structured `ParamError` when range start comes after end.                 |
"""