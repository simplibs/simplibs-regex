"""
Tests for raise_group_reference_invalid_identifier_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_group_reference_invalid_identifier_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_name", ["123abc", "my-group", "group.name", ""])
def test_raise_group_reference_invalid_identifier_error(subtests, invalid_name):
    """Verify that an invalid identifier string raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_group_reference_invalid_identifier_error,
        invalid_params=(invalid_name,),
        exception_type=ParamError,
        value=repr(invalid_name),
        label="GroupReference name",
        expected="A valid Python identifier string.",
        problem="name must be a valid identifier",
        how_to_fix="Provide a valid identifier string for the group name",
        exception=ValueError,
        verbose=False
    )