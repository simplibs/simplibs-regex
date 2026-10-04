from typing import NoReturn
from simplibs.exception import ValidationError


def raise_repeat_min_negative_error(
    min: int
) -> NoReturn:
    """Raise a structured ValidationError when repetition min count is negative."""
    raise ValidationError(
        error_name="REPEAT_MIN_NEGATIVE",
        label="min",
        value=min,
        problem=(
            f"Repeat minimum count must be at least 0, but received {min}.",
            "Repetition counts cannot be negative numbers.",
        ),
        expected="An integer greater than or equal to 0.",
        how_to_fix=(
            "Provide a non-negative integer for the `min` parameter.",
            "Example: Repeat(DIGIT, min=1)",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_repeat_min_negative_error — Repeat Min Negative Guard

## Purpose
Guards Repeat against negative minimum repetition values.
"""