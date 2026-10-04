from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_reference_numeric_out_of_range_error(
    value: int,
    low: int,
    high: int,
) -> NoReturn:
    """Raise a structured ValidationError when numeric group reference is out of range (1-99)."""
    raise ValidationError(
        error_name="GROUP_REFERENCE_NUMERIC_OUT_OF_RANGE",
        label="id_or_name",
        value=value,
        problem=(
            f"Numeric group reference {value} is out of range.",
            f"Python's regex engine supports numbered backreferences only from {low} to {high} (values >= 100 are treated as octal escapes).",
        ),
        expected=f"An integer between {low} and {high}, or a named group string.",
        how_to_fix=(
            f"Provide a group number between {low} and {high}, or use a named group reference.",
            "Example: GroupReference(5) or GroupReference('group_name')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_group_reference_numeric_out_of_range_error — Numeric Out of Range Guard

## Purpose
Guards numeric group references against exceeding the maximum supported limit of 99.
"""