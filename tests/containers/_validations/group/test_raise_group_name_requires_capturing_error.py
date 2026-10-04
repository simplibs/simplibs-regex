import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_name_requires_capturing_error,
)


def test_raise_group_name_requires_capturing_error_contract(subtests) -> None:
    """Verify that raise_group_name_requires_capturing_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_group_name_requires_capturing_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="GROUP_NAME_REQUIRES_CAPTURING",
        label="Group modifiers",
        value="name, capturing=False",
        problem=(
            "`name` requires `capturing=True` (a named group always captures).",
            "Python's `re` named groups are inherently capturing constructs.",
        ),
        expected="capturing=True when a group name is specified.",
        how_to_fix=(
            "Set `capturing=True` or omit `capturing` when providing a group `name`.",
        ),
        exception=ValueError,
        verbose=False,
    )