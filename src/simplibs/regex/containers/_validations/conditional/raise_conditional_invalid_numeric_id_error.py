from typing import NoReturn
from simplibs.exception import ParamError


def raise_conditional_invalid_numeric_id_error(
    id_or_name: int
) -> NoReturn:
    """Raise a ParamError when a conditional numeric group ID is less than 1.

    Args:
        id_or_name: The invalid integer group ID provided.

    Raises:
        ParamError: Always.
    """
    raise ParamError(
        error_name="CONDITIONAL_INVALID_NUMERIC_ID_ERROR",
        label="id_or_name",
        expected="a positive integer (>= 1)",
        value=id_or_name,
        problem=(
            f"Conditional numeric group ID must be at least 1, but received {id_or_name}.",
            "Group IDs in regular expressions start counting from 1.",
        ),
        how_to_fix=(
            "Provide a valid group number starting from 1 (e.g., 1, 2, 3).",
            "Example: Conditional(1, Literal('yes'), Literal('no'))",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_conditional_invalid_numeric_id_error — Conditional Numeric ID Guard

## Purpose
Guards Conditional against out-of-bounds negative or zero numeric group IDs.
"""