from typing import NoReturn
from simplibs.exception import ValidationError
from simplibs.regex.elements.enums import CharacterCodeKind


def raise_character_code_out_of_range_error(
    kind: CharacterCodeKind,
    value: int,
    low: int,
    high: int,
) -> NoReturn:
    """Raise a structured ValidationError when numeric char code value is out of valid range."""
    raise ValidationError(
        error_name="CHAR_CODE_OUT_OF_RANGE",
        label="value",
        value=value,
        problem=(
            f"Character code value {value} (0x{value:x}) is out of range for kind '{kind.name}'.",
            f"Allowed range for this kind is between {low} (0x{low:x}) and {high} (0x{high:x}).",
        ),
        expected=f"An integer between {low} and {high}.",
        how_to_fix=(
            f"Provide a value that fits within the valid range for {kind.name}.",
            f"Example: CharacterCode(CharacterCodeKind.{kind.name}, {low})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_code_out_of_range_error — Numeric Value Out of Range Guard

## Purpose
Guards numeric CharacterCode variants against values that exceed the permitted low/high bounds for that specific escape kind.
"""