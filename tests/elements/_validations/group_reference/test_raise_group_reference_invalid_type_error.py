"""
Tests for raise_group_reference_invalid_type_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_group_reference_invalid_type_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_target", [1.5, None, [], {}])
def test_raise_group_reference_invalid_type_error(subtests, invalid_target):
    """Verify that an unsupported type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_group_reference_invalid_type_error,
        invalid_params=(invalid_target,),
        exception_type=ParamError,
        value=type(invalid_target).__name__,
        label="GroupReference target",
        expected="An integer or string value.",
        problem="requires an int or str",
        how_to_fix="Pass an integer group number or a string group name",
        exception=TypeError,
        verbose=False
    )