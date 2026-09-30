"""
Tests for raise_group_flags_require_non_capturing_error.
"""
from simplibs.regex.containers._validations import (
    raise_group_flags_require_non_capturing_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


def test_raise_group_flags_require_non_capturing_error(subtests):
    """Verify that combining flags with capturing=True raises a ValidationError."""
    assert_exception_function(
        subtests,
        raise_group_flags_require_non_capturing_error,
        invalid_params=(),
        exception_type=ValidationError,
        value="flags, capturing=True",
        label="Group modifiers",
        expected="capturing=False when scoped flags are specified.",
        problem="`flags`/`flags_off` require `capturing=False`",
        how_to_fix="Set `capturing=False` when using `flags`",
        exception=ValueError,
        verbose=False
    )