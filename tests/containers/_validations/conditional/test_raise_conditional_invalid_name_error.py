"""
Tests for raise_conditional_invalid_name_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_conditional_invalid_name_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_str", ["123abc", "invalid-name", "foo.bar"])
def test_raise_conditional_invalid_name_error(subtests, invalid_str):
    """Verify that invalid identifier strings raise a ValidationError."""
    assert_exception_function(
        subtests,
        raise_conditional_invalid_name_error,
        invalid_params=(invalid_str,),
        exception_type=ValidationError,
        value=invalid_str,
        label="Conditional id_or_name",
        expected="A valid Python identifier string.",
        problem="name must be a valid identifier",
        how_to_fix="Ensure the group name contains only alphanumeric characters",
        exception=ValueError,
        verbose=False
    )