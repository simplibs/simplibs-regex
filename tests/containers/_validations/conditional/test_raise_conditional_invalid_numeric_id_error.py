"""
Tests for raise_conditional_invalid_numeric_id_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_conditional_invalid_numeric_id_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_int", [0, -1, -5])
def test_raise_conditional_invalid_numeric_id_error(subtests, invalid_int):
    """Verify that non-positive group IDs raise a ValidationError."""
    assert_exception_function(
        subtests,
        raise_conditional_invalid_numeric_id_error,
        invalid_params=(invalid_int,),
        exception_type=ValidationError,
        value=invalid_int,
        label="Conditional id_or_name",
        expected="An integer >= 1.",
        problem="numeric id must be >= 1",
        how_to_fix="Provide a group index starting from 1.",
        exception=ValueError,
        verbose=False
    )