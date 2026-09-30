"""
Tests for raise_literal_empty_error.
"""
from simplibs.regex.elements._validations import (
    raise_literal_empty_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


def test_raise_literal_empty_error(subtests):
    """Verify that an empty string raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_literal_empty_error,
        invalid_params=(),
        exception_type=ParamError,
        value="''",
        label="Literal text",
        expected="A non-string with len >= 1.",
        problem="requires a non-empty string",
        how_to_fix="Provide a non-empty string for the Literal",
        exception=ValueError,
        verbose=False
    )