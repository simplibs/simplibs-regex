"""
Tests for raise_repeat_max_less_than_min_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_repeat_max_less_than_min_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("min_val, max_val", [(2, 1), (5, 0), (10, 9)])
def test_raise_repeat_max_less_than_min_error(subtests, min_val, max_val):
    """Verify that max < min raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_repeat_max_less_than_min_error,
        invalid_params=(min_val, max_val),
        exception_type=ParamError,
        value=f"min={min_val}, max={max_val}",
        label="Repeat bounds",
        expected="max >= min.",
        problem="requires max >= min",
        how_to_fix="Ensure `max` is greater than or equal to `min`",
        exception=ValueError,
        verbose=False
    )