import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_locale_flag_unsupported_error,
)


def test_raise_locale_flag_unsupported_error_contract(subtests) -> None:
    """Verify that raise_locale_flag_unsupported_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_locale_flag_unsupported_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="LOCALE_FLAG_UNSUPPORTED",
        label="flags",
        value="Flag.LOCALE",
        problem=(
            "`Flag.LOCALE` is not supported with string-based regular expressions in Python.",
            "Python's `re` module restricts LOCALE flag usage, and this library exclusively uses string patterns.",
        ),
        expected="Avoid using Flag.LOCALE in regex flags.",
        how_to_fix=(
            "Remove `Flag.LOCALE` from the `flags` parameter set.",
            "Example: Group(inner, flags={Flag.IGNORECASE})",
        ),
        exception=ValueError,
        verbose=False,
    )