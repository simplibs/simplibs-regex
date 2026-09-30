"""
Tests for raise_group_atomic_and_flags_conflict_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_atomic_and_flags_conflict_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_atomic_and_flags_conflict_error(subtests):
    """Verify that combining atomic and flags raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_atomic_and_flags_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="atomic=True, flags",
        label="Group modifiers",
        expected="Only one structural modifier (atomic or flags) per group.",
        problem="`atomic=True` cannot be combined with `flags`/`flags_off`",
        how_to_fix="Separate scoped flags and atomic grouping",
        exception=ValueError,
        verbose=False
    )