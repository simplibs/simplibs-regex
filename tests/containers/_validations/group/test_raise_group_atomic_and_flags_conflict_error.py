import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_atomic_and_flags_conflict_error,
)


def test_raise_group_atomic_and_flags_conflict_error_contract(subtests) -> None:
    """Verify that raise_group_atomic_and_flags_conflict_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_atomic_and_flags_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_ATOMIC_AND_FLAGS_CONFLICT",
        label="Group modifiers",
        value="atomic=True, flags",
        problem=(
            "`atomic=True` cannot be combined with `flags`/`flags_off`.",
            "Python's `re` syntax does not support scoped flags inside an atomic group opening.",
        ),
        expected="Only one structural modifier (atomic or flags) per group.",
        how_to_fix=(
            "Separate scoped flags and atomic grouping into nested groups.",
        ),
        exception=ValueError,
        verbose=False,
    )