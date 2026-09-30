"""
Tests for raise_repeat_invalid_mode_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_repeat_invalid_mode_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_mode", ["greedy", "lazy", 1, None])
def test_raise_repeat_invalid_mode_error(subtests, invalid_mode):
    """Verify that an invalid mode type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_repeat_invalid_mode_error,
        invalid_params=(invalid_mode,),
        exception_type=ParamError,
        value=type(invalid_mode).__name__,
        label="Repeat mode",
        expected="A RepeatMode instance",
        problem="requires a RepeatMode for `mode`",
        how_to_fix="Pass an explicit RepeatMode enum value",
        exception=TypeError,
        verbose=False
    )