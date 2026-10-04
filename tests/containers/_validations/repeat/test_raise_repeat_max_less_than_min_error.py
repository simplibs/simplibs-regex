import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_repeat_max_less_than_min_error,
)


@pytest.mark.parametrize(
    "min_val, max_val",
    [
        (5, 3),
        (2, 0),
        (1, 0),
    ],
)
def test_raise_repeat_max_less_than_min_error_contract(
    subtests,
    min_val,
    max_val,
) -> None:
    """Verify that raise_repeat_max_less_than_min_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_repeat_max_less_than_min_error,
        invalid_params=(min_val, max_val),
        exception_type=ValidationError,
        error_name="REPEAT_MAX_LESS_THAN_MIN",
        label="max",
        value=max_val,
        problem=(
            f"Repeat maximum count ({max_val}) cannot be less than minimum count ({min_val}).",
            "The upper bound of a range repetition must be greater than or equal to the lower bound.",
        ),
        expected=f"An integer greater than or equal to min ({min_val}).",
        how_to_fix=(
            f"Ensure `max` is greater than or equal to {min_val}, or omit `max` for unbounded repetition.",
            f"Example: Repeat(DIGIT, min={min_val}, max={min_val + 2})",
        ),
        exception=ValueError,
        verbose=False,
    )