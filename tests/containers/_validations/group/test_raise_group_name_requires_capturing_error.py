"""
Tests for raise_group_name_requires_capturing_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_name_requires_capturing_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_name_requires_capturing_error(subtests):
    """Verify that combining name with capturing=False raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_name_requires_capturing_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="name, capturing=False",
        label="Group modifiers",
        expected="capturing=True when a group name is specified.",
        problem="`name` requires `capturing=True`",
        how_to_fix="Set `capturing=True` or omit `capturing`",
        exception=ValueError,
        verbose=False
    )