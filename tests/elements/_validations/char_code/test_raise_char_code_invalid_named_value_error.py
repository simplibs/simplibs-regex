"""
Tests for raise_char_code_invalid_named_value_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_char_code_invalid_named_value_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_value", ["", 123, None, []])
def test_raise_char_code_invalid_named_value_error(subtests, invalid_value):
    """Verify that an invalid named value raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_code_invalid_named_value_error,
        invalid_params=(invalid_value,),
        exception_type=ParamError,
        value=repr(invalid_value),
        label="CharCode named value",
        expected="A non-empty string",
        problem="requires a non-empty str name",
        how_to_fix="Provide a valid non-empty string name",
        exception=ValueError,
        verbose=False
    )