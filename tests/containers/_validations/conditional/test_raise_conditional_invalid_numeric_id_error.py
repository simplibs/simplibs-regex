import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_conditional_invalid_numeric_id_error,
)


@pytest.mark.parametrize(
    "invalid_id",
    [
        0,
        -1,
        -5,
        -100,
    ],
)
def test_raise_conditional_invalid_numeric_id_error_contract(
    subtests,
    invalid_id,
) -> None:
    """Verify that raise_conditional_invalid_numeric_id_error raises ParamError
    wrapping ValueError when a conditional numeric group ID is less than 1."""

    assert_exception_function(
        subtests,
        raise_conditional_invalid_numeric_id_error,
        invalid_params=(invalid_id,),
        exception_type=ParamError,
        error_name="CONDITIONAL_INVALID_NUMERIC_ID_ERROR",
        label="id_or_name",
        expected="a positive integer (>= 1)",
        value=invalid_id,
        problem=(
            f"Conditional numeric group ID must be at least 1, but received {invalid_id}.",
            "Group IDs in regular expressions start counting from 1.",
        ),
        how_to_fix=(
            "Provide a valid group number starting from 1 (e.g., 1, 2, 3).",
            "Example: Conditional(1, Literal('yes'), Literal('no'))",
        ),
        exception=ValueError,
        verbose=False,
    )