import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_repeat_min_negative_error,
)


@pytest.mark.parametrize(
    "invalid_min",
    [-1, -5, -10],
)
def test_raise_repeat_min_negative_error_contract(
    subtests,
    invalid_min,
) -> None:
    """Verify that raise_repeat_min_negative_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_repeat_min_negative_error,
        invalid_params=(invalid_min,),
        exception_type=ValidationError,
        error_name="REPEAT_MIN_NEGATIVE",
        label="min",
        value=invalid_min,
        problem=(
            f"Repeat minimum count must be at least 0, but received {invalid_min}.",
            "Repetition counts cannot be negative numbers.",
        ),
        expected="An integer greater than or equal to 0.",
        how_to_fix=(
            "Provide a non-negative integer for the `min` parameter.",
            "Example: Repeat(DIGIT, min=1)",
        ),
        exception=ValueError,
        verbose=False,
    )