from .raise_character_code_invalid_kind_error import raise_character_code_invalid_kind_error
from .raise_character_code_invalid_named_value_error import raise_character_code_invalid_named_value_error
from .raise_character_code_invalid_type_error import raise_character_code_invalid_type_error
from .raise_character_code_out_of_range_error import raise_character_code_out_of_range_error
from .raise_character_code_unknown_name_error import raise_character_code_unknown_name_error

_DESIGN_NOTES = """
# CharacterCode Validations Sub-Package

## Purpose
Provides structured exception emission helpers for CharacterCode validation.

## Internal Components Registry

| Component                                          | Type     | Description                                                                          |
| :------------------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `raise_character_code_invalid_kind_error`          | Function | Emits structured `ValidationError` when a CharacterCode receives an invalid kind.    |
| `raise_character_code_invalid_named_value_error`   | Function | Emits structured `ParamError` when a named CharacterCode receives an invalid value.  |
| `raise_character_code_invalid_type_error`          | Function | Emits structured `ParamError` when a numeric CharacterCode receives a non-int type.  |
| `raise_character_code_out_of_range_error`          | Function | Emits structured `ParamError` when a numeric CharacterCode value is out of range.    |
| `raise_character_code_unknown_name_error`          | Function | Emits structured `ParamError` when a named CharacterCode receives an unknown name.   |
"""