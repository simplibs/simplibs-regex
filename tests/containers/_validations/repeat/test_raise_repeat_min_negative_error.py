"""
Tests for raise_repeat_min_negative_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_repeat_min_negative_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_min", [-1, -5, -100])
def test_raise_repeat_min_negative_error(subtests, invalid_min):
    """Verify that a negative min raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_repeat_min_negative_error,
        invalid_params=(invalid_min,),
        exception_type=ParamError,
        value=invalid_min,
        label="Repeat min",
        expected="An integer greater than or equal to 0.",
        problem="requires min >= 0",
        how_to_fix="Provide a non-negative integer",
        exception=ValueError,
        verbose=False
    )