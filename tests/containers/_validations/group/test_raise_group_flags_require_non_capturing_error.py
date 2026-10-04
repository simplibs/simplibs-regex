import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_flags_require_non_capturing_error,
)


def test_raise_group_flags_require_non_capturing_error_contract(subtests) -> None:
    """Verify that raise_group_flags_require_non_capturing_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_flags_require_non_capturing_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_FLAGS_REQUIRE_NON_CAPTURING",
        label="Group modifiers",
        value="flags, capturing=True",
        problem=(
            "`flags`/`flags_off` require `capturing=False` — Python's `re` scoped-flag syntax `(?flags:...)` is always non-capturing.",
            "Scoped flag groups in Python regex cannot capture text.",
        ),
        expected="capturing=False when scoped flags are specified.",
        how_to_fix=(
            "Set `capturing=False` when using `flags` or `flags_off`.",
        ),
        exception=ValueError,
        verbose=False,
    )