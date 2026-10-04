import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.compiler._validations import (
    raise_invalid_locale_error,
)


@pytest.mark.parametrize(
    "flags",
    [
        frozenset(["LOCALE"]),
        {"LOCALE", "IGNORECASE"},
        "LOCALE_FLAG_MOCK",
    ],
)
def test_raise_invalid_locale_error_contract(
    subtests,
    flags,
) -> None:
    """Verify that raise_invalid_locale_error raises ParamError
    wrapping ValueError when Flag.LOCALE is improperly used."""

    assert_exception_function(
        subtests,
        raise_invalid_locale_error,
        invalid_params=(flags,),
        exception_type=ParamError,
        error_name="INVALID_LOCALE_ERROR",
        label="flags",
        expected="flags excluding Flag.LOCALE for string patterns",
        value=flags,
        problem=(
            "Flag.LOCALE cannot be used with string pattern compilation.",
            f"Received flags collection containing Flag.LOCALE: {flags!r}.",
        ),
        how_to_fix=(
            "Remove Flag.LOCALE from the flags set.",
            "Use standard flags (like IGNORECASE, MULTILINE) instead.",
        ),
        exception=ValueError,
        verbose=False,
    )