from typing import Any, NoReturn
from simplibs.exception import ValidationError
from simplibs.regex.elements.enums import CharacterCodeKind


def raise_character_code_invalid_type_error(kind: CharacterCodeKind, value: Any) -> NoReturn:
    """Raise a structured ValidationError when numeric char code value has an invalid type (like bool)."""
    raise ValidationError(
        error_name="CHAR_CODE_INVALID_TYPE",
        label="value",
        value=value,
        problem=(
            f"Invalid value type for character code kind '{kind.name}': received {value!r} (type {type(value).__name__}).",
            "Booleans and non-integer types are not permitted as numeric character codes.",
        ),
        expected="An integer value within the valid range for the specified character code kind.",
        how_to_fix=(
            "Provide an integer value instead of a boolean or other type.",
            "Example: CharacterCode(CharacterCodeKind.HEX, 0x41)",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_character_code_invalid_type_error — Invalid Numeric Type Guard

## Purpose
Guards numeric CharacterCode variants against incorrect types such as booleans or non-integers.
"""