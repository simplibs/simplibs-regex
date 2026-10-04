import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_flags_off_without_flags_error,
)


def test_raise_group_flags_off_without_flags_error_contract(subtests) -> None:
    """Verify that raise_group_flags_off_without_flags_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_flags_off_without_flags_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_FLAGS_OFF_WITHOUT_FLAGS",
        label="Group modifiers",
        value="flags_off without flags",
        problem=(
            "`flags_off` was given without `flags` — pass the flags that stay ON explicitly, even if empty via `flags=frozenset()`.",
            "Implicit flag states are disallowed to ensure call-site readability.",
        ),
        expected="Explicit `flags` parameter accompanying `flags_off`.",
        how_to_fix=(
            "Provide `flags=frozenset()` or active flags alongside `flags_off`.",
        ),
        exception=ValueError,
        verbose=False,
    )