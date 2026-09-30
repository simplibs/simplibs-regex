from .raise_character_type_invalid_kind_error import raise_character_type_invalid_kind_error

_DESIGN_NOTES = """
# CharacterType Validations Sub-Package

## Purpose
Provides structured exception emission helpers for CharacterType validation.

## Internal Components Registry

| Component                                     | Type     | Description                                                                     |
| :-------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_character_type_invalid_kind_error`     | Function | Emits structured `ParamError` when an invalid CharacterTypeKind is received.    |
"""