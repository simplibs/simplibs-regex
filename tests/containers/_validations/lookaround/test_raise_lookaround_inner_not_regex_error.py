"""
Tests for raise_lookaround_inner_not_regex_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_lookaround_inner_not_regex_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_inner", ["raw_string", 123, None, object()])
def test_raise_lookaround_inner_not_regex_error(subtests, invalid_inner):
    """Verify that a non-Regex inner node raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_lookaround_inner_not_regex_error,
        invalid_params=(invalid_inner,),
        exception_type=ParamError,
        value=type(invalid_inner).__name__,
        label="Lookaround inner",
        expected="A valid Regex instance.",
        problem="requires a Regex instance for `inner`",
        how_to_fix="Wrap raw strings or objects into appropriate atom classes",
        exception=TypeError,
        verbose=False
    )