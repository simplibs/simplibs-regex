from typing import NoReturn
from simplibs.exception import ValidationError


def raise_literal_empty_error() -> NoReturn:
    """Raise a structured ValidationError when literal text is empty."""
    raise ValidationError(
        error_name="LITERAL_EMPTY",
        label="text",
        value="",
        problem=(
            "Literal text cannot be an empty string.",
            "An empty literal has no matching behavior and is invalid in regular expression patterns.",
        ),
        expected="A non-empty string (e.g., 'abc', 'x').",
        how_to_fix=(
            "Provide a non-empty string for the Literal element.",
            "Example: Literal('text')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_literal_empty_error — Empty Literal Guard

## Purpose
Guards Literal against being initialized with an empty string.
"""