from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_character_type_invalid_kind_error(kind: Any) -> NoReturn:
    """Raise a structured ParamError when CharacterType() receives an invalid kind type."""
    raise ParamError(
        error_name="CHARACTER_TYPE_INVALID_KIND",
        label="CharacterType kind",
        value=type(kind).__name__,
        problem=(
            f"CharacterType() requires a CharacterTypeKind, got {kind!r} of type '{type(kind).__name__}'.",
            "The kind parameter must be a valid member of the CharacterTypeKind enumeration.",
        ),
        expected="A CharacterTypeKind instance (e.g. CharacterTypeKind.DIGIT).",
        how_to_fix=(
            "Pass an explicit CharacterTypeKind enum value.",
        ),
        exception=TypeError,
    )