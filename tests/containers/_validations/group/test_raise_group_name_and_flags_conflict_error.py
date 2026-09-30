"""
Tests for raise_group_name_and_flags_conflict_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_name_and_flags_conflict_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_name_and_flags_conflict_error(subtests):
    """Verify that combining name and flags raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_name_and_flags_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="name, flags",
        label="Group modifiers",
        expected="Only one structural modifier (name or flags) per group.",
        problem="`name` cannot be combined with `flags`/`flags_off`",
        how_to_fix="Apply flags in an enclosing group",
        exception=ValueError,
        verbose=False
    )