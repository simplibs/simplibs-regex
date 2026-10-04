from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_character_range_invalid_boundary_error(
    name: str,
    value: Any,
) -> None:
    """Raise a structured ValidationError when a character range boundary is not a single character."""
    received_type = type(value).__name__

    raise ValidationError(
        error_name="CHARACTER_RANGE_INVALID_BOUNDARY",
        label=name,
        value=value,
        problem=(
            f"Character range boundary '{name}' must be a single-character string, but received value {value!r} of type '{received_type}'.",
            "Character ranges (`a-z`) can only span between individual single characters.",
        ),
        expected="A single-character string (e.g., 'a', 'Z', '0').",
        how_to_fix=(
            f"Provide a single character for the `{name}` boundary.",
            "Example: CharacterRange('a', 'z')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_range_invalid_boundary_error — Invalid Range Boundary Guard

## Purpose
Guards CharacterRange against boundary values that are not single characters (e.g., empty strings or multi-character strings).
"""