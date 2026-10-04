import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_atomic_and_name_conflict_error,
)


def test_raise_group_atomic_and_name_conflict_error_contract(subtests) -> None:
    """Verify that raise_group_atomic_and_name_conflict_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_atomic_and_name_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_ATOMIC_AND_NAME_CONFLICT",
        label="Group modifiers",
        value="atomic=True, name",
        problem=(
            "`atomic=True` cannot be combined with `name`.",
            "Python's `re` syntax does not support atomic named groups in a single construct.",
        ),
        expected="Only one structural modifier (atomic or name) per group.",
        how_to_fix=(
            "Use either an atomic group or a named group, but not both simultaneously.",
        ),
        exception=ValueError,
        verbose=False,
    )