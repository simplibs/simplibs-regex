from typing import NoReturn
from simplibs.exception import ValidationError


def raise_repeat_max_less_than_min_error(
    min: int,
    max: int,
) -> NoReturn:
    """Raise a structured ValidationError when repetition max count is less than min count."""
    raise ValidationError(
        error_name="REPEAT_MAX_LESS_THAN_MIN",
        label="max",
        value=max,
        problem=(
            f"Repeat maximum count ({max}) cannot be less than minimum count ({min}).",
            "The upper bound of a range repetition must be greater than or equal to the lower bound.",
        ),
        expected=f"An integer greater than or equal to min ({min}).",
        how_to_fix=(
            f"Ensure `max` is greater than or equal to {min}, or omit `max` for unbounded repetition.",
            f"Example: Repeat(DIGIT, min={min}, max={min + 2})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_repeat_max_less_than_min_error — Repeat Max Less Than Min Guard

## Purpose
Guards Repeat against invalid ranges where max is smaller than min.
"""