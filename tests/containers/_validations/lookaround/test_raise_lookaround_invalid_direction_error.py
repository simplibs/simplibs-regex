"""
Tests for raise_lookaround_invalid_direction_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_lookaround_invalid_direction_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_direction", ["ahead", "behind", 123, None])
def test_raise_lookaround_invalid_direction_error(subtests, invalid_direction):
    """Verify that an invalid direction type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_lookaround_invalid_direction_error,
        invalid_params=(invalid_direction,),
        exception_type=ParamError,
        value=type(invalid_direction).__name__,
        label="Lookaround direction",
        expected="A LookaroundDirection instance",
        problem="requires a LookaroundDirection for `direction`",
        how_to_fix="Pass an explicit LookaroundDirection enum value",
        exception=TypeError,
        verbose=False
    )