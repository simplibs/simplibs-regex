from .raise_char_class_empty_error import raise_char_class_empty_error
from .raise_char_class_item_not_allowed_error import raise_char_class_item_not_allowed_error
from .raise_multi_char_literal_in_char_class_error import raise_multi_char_literal_in_char_class_error

_DESIGN_NOTES = """
# CharacterClass Validations Sub-Package

## Purpose
Provides structured exception emission helpers for CharacterClass validation.

## Internal Components Registry

| Component                                      | Type     | Description                                                                     |
| :--------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_char_class_empty_error`                 | Function | Emits structured `ParamError` when a CharacterClass is empty.                   |
| `raise_char_class_item_not_allowed_error`      | Function | Emits structured `ParamError` when an item is not allowed in a CharacterClass.  |
| `raise_multi_char_literal_in_char_class_error` | Function | Emits structured `ParamError` when a multi-character literal is used in a class.|
"""