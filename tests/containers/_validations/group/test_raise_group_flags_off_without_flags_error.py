"""
Tests for raise_group_flags_off_without_flags_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_flags_off_without_flags_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_flags_off_without_flags_error(subtests):
    """Verify that flags_off without flags raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_flags_off_without_flags_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="flags_off without flags",
        label="Group modifiers",
        expected="Explicit `flags` parameter accompanying `flags_off`.",
        problem="`flags_off` was given without `flags`",
        how_to_fix="Provide `flags=frozenset()` or active flags",
        exception=ValueError,
        verbose=False
    )