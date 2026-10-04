from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_character_code_invalid_named_value_error(value: Any) -> NoReturn:
    """Raise a structured ValidationError when a named character code value is empty or invalid."""
    raise ValidationError(
        error_name="CHAR_CODE_INVALID_NAMED_VALUE",
        label="value",
        value=value,
        problem=(
            f"Invalid named character code value: {value!r}.",
            "Named character escapes (`\\N{NAME}`) require a non-empty Unicode character name string.",
        ),
        expected="A non-empty string representing a Unicode character name.",
        how_to_fix=(
            "Provide a valid non-empty string for the character name.",
            "Example: CharacterCode(CharacterCodeKind.NAMED, 'BULLET')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_code_invalid_named_value_error — Invalid Named Character Value Guard

## Purpose
Guards CharacterCode against empty or invalid string values passed to named character code escapes (`\\N{NAME}`).
"""