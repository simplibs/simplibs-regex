from typing import NoReturn
from simplibs.exception import ParamError


def raise_group_reference_numeric_out_of_range_error(id_or_name: int) -> NoReturn:
    """Raise a structured ParamError when GroupReference numeric id is less than 1."""
    raise ParamError(
        error_name="GROUP_REFERENCE_NUMERIC_OUT_OF_RANGE",
        label="GroupReference numeric id",
        value=str(id_or_name),
        problem=(
            f"GroupReference() numeric id must be >= 1, got {id_or_name}.",
            "Group reference numbers must be positive integers starting from 1.",
        ),
        expected="An integer >= 1.",
        how_to_fix=(
            "Provide a valid group number greater than or equal to 1.",
        ),
        exception=ValueError,
    )