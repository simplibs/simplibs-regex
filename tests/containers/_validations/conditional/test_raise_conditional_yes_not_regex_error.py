"""
Tests for raise_conditional_yes_not_regex_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_conditional_yes_not_regex_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_yes", ["raw_string", 123, object()])
def test_raise_conditional_yes_not_regex_error(subtests, invalid_yes):
    """Verify that a non-Regex yes branch raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_conditional_yes_not_regex_error,
        invalid_params=(invalid_yes,),
        exception_type=ParamError,
        value=type(invalid_yes).__name__,
        label="Conditional yes",
        expected="A valid Regex instance.",
        problem="requires a Regex instance for `yes`",
        how_to_fix="Wrap raw strings or objects into appropriate atom classes",
        exception=TypeError,
        verbose=False
    )