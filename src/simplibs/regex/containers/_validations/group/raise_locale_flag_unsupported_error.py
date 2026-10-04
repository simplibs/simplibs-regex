from typing import NoReturn
from simplibs.exception import ValidationError


def raise_locale_flag_unsupported_error() -> NoReturn:
    """Raise a structured ValidationError when Flag.LOCALE is used."""
    raise ValidationError(
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
    )


_DESIGN_NOTES = """
# raise_locale_flag_unsupported_error — Unsupported Locale Flag Guard

## Purpose
Guards against passing Flag.LOCALE which causes issues with string patterns in Python's regex engine.
"""