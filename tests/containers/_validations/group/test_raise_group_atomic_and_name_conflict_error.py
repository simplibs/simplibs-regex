"""
Tests for raise_group_atomic_and_name_conflict_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_atomic_and_name_conflict_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_atomic_and_name_conflict_error(subtests):
    """Verify that combining atomic and name raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_atomic_and_name_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="atomic=True, name",
        label="Group modifiers",
        expected="Only one structural modifier (atomic or name) per group.",
        problem="`atomic=True` cannot be combined with `name`",
        how_to_fix="Use either an atomic group or a named group",
        exception=ValueError,
        verbose=False
    )