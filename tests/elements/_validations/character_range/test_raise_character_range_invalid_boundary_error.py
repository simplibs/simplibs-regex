"""
Tests for raise_character_range_invalid_boundary_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_character_range_invalid_boundary_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_value", ["ab", "", 123, None])
def test_raise_character_range_invalid_boundary_error(subtests, invalid_value):
    """Verify that a non-single-character boundary raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_character_range_invalid_boundary_error,
        invalid_params=("start", invalid_value),
        exception_type=ParamError,
        value=repr(invalid_value),
        label="CharacterRange start",
        expected="A single-character string (len == 1).",
        problem="requires `start` to be a single character",
        how_to_fix="Provide a single character for both `start` and `end` boundaries",
        exception=ValueError,
        verbose=False
    )