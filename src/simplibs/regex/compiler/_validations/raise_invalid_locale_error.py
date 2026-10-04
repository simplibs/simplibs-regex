from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_invalid_locale_error(
    flags: Any
) -> NoReturn:
    """Raise a ParamError when Flag.LOCALE is included in flags,
    as LOCALE cannot be used with string pattern compilation.

    Args:
        flags: The invalid flags collection provided.

    Raises:
        ParamError: Always.
    """
    raise ParamError(
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
    )


_DESIGN_NOTES = """
# raise_invalid_locale_error — RegexPattern Locale Flag Guard

## Purpose
Guards RegexPattern's precondition that Flag.LOCALE cannot be combined
with structured string regex compilation.
"""