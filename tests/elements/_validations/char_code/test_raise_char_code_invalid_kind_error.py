"""
Tests for raise_char_code_invalid_kind_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_char_code_invalid_kind_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_kind", ["HEX", "\\xFF", 123, None])
def test_raise_char_code_invalid_kind_error(subtests, invalid_kind):
    """Verify that an invalid kind type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_code_invalid_kind_error,
        invalid_params=(invalid_kind,),
        exception_type=ParamError,
        value=type(invalid_kind).__name__,
        label="CharCode kind",
        expected="A CharCodeKind instance",
        problem="requires a CharCodeKind",
        how_to_fix="Pass an explicit CharCodeKind enum value",
        exception=TypeError,
        verbose=False
    )