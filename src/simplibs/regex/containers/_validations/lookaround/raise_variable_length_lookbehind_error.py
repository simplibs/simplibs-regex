from typing import NoReturn
from simplibs.exception import ValidationError
from simplibs.regex.base_class import Regex


def raise_variable_length_lookbehind_error(
    inner: Regex
) -> NoReturn:
    """Raise a structured ValidationError when a lookbehind assertion has a variable length."""
    raise ValidationError(
        error_name="VARIABLE_LENGTH_LOOKBEHIND",
        label="inner",
        value=inner,
        problem=(
            "Lookbehind assertions (`(?<=...)` and `(?<!...)`) require a fixed-length inner pattern.",
            "The provided inner pattern has a variable or unknown length.",
        ),
        expected="An inner regex pattern with a fixed length.",
        how_to_fix=(
            "Ensure the inner pattern uses only fixed-length components (e.g., specific counts instead of quantifiers like `*` or `+`).",
            "Example: Lookaround(DIGIT, direction=LookaroundDirection.BEHIND)",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_variable_length_lookbehind_error — Variable-Length Lookbehind Guard

## Purpose
Guards Lookaround against variable-length expressions inside lookbehind assertions, which Python's regex engine rejects.
"""