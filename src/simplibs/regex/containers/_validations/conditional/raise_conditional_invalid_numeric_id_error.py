from typing import NoReturn
from simplibs.exception import ValidationError


def raise_conditional_invalid_numeric_id_error(id_or_name: int) -> NoReturn:
    """Raise a structured ValidationError when Conditional() numeric id is less than 1."""
    raise ValidationError(
        error_name="CONDITIONAL_INVALID_NUMERIC_ID",
        label="Conditional id_or_name",
        value=id_or_name,
        problem=(
            f"Conditional() numeric id must be >= 1, got {id_or_name}.",
            "Group reference numbers in conditional patterns must be positive integers.",
        ),
        expected="An integer >= 1.",
        how_to_fix=(
            "Provide a group index starting from 1.",
        ),
        exception=ValueError,
    )