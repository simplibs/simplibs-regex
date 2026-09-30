"""
Tests for raise_literal_invalid_type_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_literal_invalid_type_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_text", [123, 45.6, None, []])
def test_raise_literal_invalid_type_error(subtests, invalid_text):
    """Verify that a non-string value raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_literal_invalid_type_error,
        invalid_params=(invalid_text,),
        exception_type=ParamError,
        value=type(invalid_text).__name__,
        label="Literal text",
        expected="A string value.",
        problem="requires a str",
        how_to_fix="Pass a string to the Literal constructor",
        exception=TypeError,
        verbose=False
    )