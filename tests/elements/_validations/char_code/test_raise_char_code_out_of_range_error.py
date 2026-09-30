"""
Tests for raise_char_code_out_of_range_error.
"""
import pytest
from simplibs.regex.elements.CharCode import CharCodeKind
from simplibs.regex.elements._validations import (
    raise_char_code_out_of_range_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("value, low, high", [(300, 0, 255), (-1, 0, 255)])
def test_raise_char_code_out_of_range_error(subtests, value, low, high):
    """Verify that an out-of-range value raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_code_out_of_range_error,
        invalid_params=(CharCodeKind.HEX, value, low, high),
        exception_type=ParamError,
        value=str(value),
        label="CharCode HEX range",
        expected=f"A value between {low} and {high}.",
        problem="is invalid — expected",
        how_to_fix="Provide a numeric value within the range",
        exception=ValueError,
        verbose=False
    )