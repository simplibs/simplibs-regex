"""
Tests for raise_char_class_empty_error.
"""
from simplibs.regex.elements._validations import (
    raise_char_class_empty_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


def test_raise_char_class_empty_error(subtests):
    """Verify that an empty character class raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_class_empty_error,
        invalid_params=(),
        exception_type=ParamError,
        value="none",
        label="CharacterClass items",
        expected="At least one valid regex item for the character class.",
        problem="requires at least one item",
        how_to_fix="Provide one or more items",
        exception=ValueError,
        verbose=False
    )