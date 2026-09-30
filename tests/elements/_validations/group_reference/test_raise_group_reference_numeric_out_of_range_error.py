"""
Tests for raise_group_reference_numeric_out_of_range_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_group_reference_numeric_out_of_range_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_id", [0, -1, -5])
def test_raise_group_reference_numeric_out_of_range_error(subtests, invalid_id):
    """Verify that a numeric id < 1 raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_group_reference_numeric_out_of_range_error,
        invalid_params=(invalid_id,),
        exception_type=ParamError,
        value=str(invalid_id),
        label="GroupReference numeric id",
        expected="An integer >= 1.",
        problem="numeric id must be >= 1",
        how_to_fix="Provide a valid group number greater than or equal to 1",
        exception=ValueError,
        verbose=False
    )