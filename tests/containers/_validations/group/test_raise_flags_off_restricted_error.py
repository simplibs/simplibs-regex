import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_flags_off_restricted_error,
)
from simplibs.regex.flags.Flag import Flag


def test_raise_flags_off_restricted_error_contract(subtests) -> None:
    """Verify that raise_flags_off_restricted_error raises ValidationError wrapping ValueError."""
    restricted_flags = frozenset({Flag.ASCII})
    formatted_flags = "ASCII"

    assert_exception_function(
        subtests,
        raise_flags_off_restricted_error,
        invalid_params=(restricted_flags,),
        exception_type=ValidationError,
        error_name="FLAGS_OFF_RESTRICTED",
        label="flags_off",
        value=formatted_flags,
        problem=(
            f"The following flags cannot be turned off in Python's regex: {formatted_flags}.",
            "Python's `re` module only permits turning off IGNORECASE, MULTILINE, DOTALL, and VERBOSE.",
        ),
        expected="Only turnable-off flags in `flags_off` (ASCII, LOCALE, and UNICODE cannot be turned off).",
        how_to_fix=(
            "Remove ASCII, LOCALE, or UNICODE from the `flags_off` set.",
            "Example: Group(inner, flags={Flag.ASCII}, flags_off={Flag.IGNORECASE})",
        ),
        exception=ValueError,
        verbose=False,
    )