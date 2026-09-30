"""
Tests for raise_conditional_no_not_regex_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_conditional_no_not_regex_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_no", ["raw_string", 123, object()])
def test_raise_conditional_no_not_regex_error(subtests, invalid_no):
    """Verify that an invalid no branch type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_conditional_no_not_regex_error,
        invalid_params=(invalid_no,),
        exception_type=ParamError,
        value=type(invalid_no).__name__,
        label="Conditional no",
        expected="A valid Regex instance or None.",
        problem="requires a Regex instance or None for `no`",
        how_to_fix="Wrap raw strings or objects into appropriate atom classes",
        exception=TypeError,
        verbose=False
    )