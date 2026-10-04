import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_ascii_unicode_conflict_error,
)


def test_raise_group_ascii_unicode_conflict_error_contract(subtests) -> None:
    """Verify that raise_group_ascii_unicode_conflict_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_ascii_unicode_conflict_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_ASCII_UNICODE_CONFLICT",
        label="flags",
        value="ASCII, UNICODE",
        problem=(
            "`Flag.ASCII` and `Flag.UNICODE` cannot both be active simultaneously in a group.",
            "Python's regex engine treats ASCII and UNICODE character matching modes as mutually exclusive.",
        ),
        expected="Only one character-encoding flag (ASCII or UNICODE) per group.",
        how_to_fix=(
            "Keep either Flag.ASCII or Flag.UNICODE in `flags`, but not both.",
            "Example: Group(inner, flags={Flag.ASCII})",
        ),
        exception=ValueError,
        verbose=False,
    )