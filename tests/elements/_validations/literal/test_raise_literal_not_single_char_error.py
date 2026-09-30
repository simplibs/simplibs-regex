"""
Tests for raise_literal_not_single_char_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_literal_not_single_char_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_text", ["abc", "hello", "12"])
def test_raise_literal_not_single_char_error(subtests, invalid_text):
    """Verify that a multi-character literal char class fragment raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_literal_not_single_char_error,
        invalid_params=(invalid_text,),
        exception_type=ParamError,
        value=invalid_text,
        label="Literal char class fragment",
        expected="A single-character Literal (len == 1).",
        problem="is not a single character",
        how_to_fix="Ensure only single-character literals are used inside character classes",
        exception=ValueError,
        verbose=False
    )