"""
Tests for raise_char_code_invalid_type_error.
"""
import pytest
from simplibs.regex.elements.CharCode import CharCodeKind
from simplibs.regex.elements._validations import (
    raise_char_code_invalid_type_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_value", ["0x41", 65.5, None, []])
def test_raise_char_code_invalid_type_error(subtests, invalid_value):
    """Verify that a non-integer numeric value raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_code_invalid_type_error,
        invalid_params=(CharCodeKind.HEX, invalid_value),
        exception_type=ParamError,
        value=type(invalid_value).__name__,
        label="CharCode HEX value",
        expected="An integer value.",
        problem="requires an int value",
        how_to_fix="Pass an integer representing the character code",
        exception=TypeError,
        verbose=False
    )