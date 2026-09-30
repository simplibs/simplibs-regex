"""
Tests for raise_invalid_group_name_error — validation of named group identifiers.
"""
import pytest

from simplibs.regex.containers._validations import (
    raise_invalid_group_name_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_name", ["123invalid", "my-group", "group.name", "", 42])
def test_raise_invalid_group_name_error(subtests, invalid_name):
    """Verify that invalid group names raise a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_invalid_group_name_error,
        invalid_params=(invalid_name,),
        exception_type=ParamError,
        value=invalid_name,
        label="group name",
        expected="A non-empty string that forms a valid Python identifier",
        problem="not a valid identifier",
        how_to_fix="Provide a valid string identifier for the group name",
        exception=ValueError,
        verbose=False
    )