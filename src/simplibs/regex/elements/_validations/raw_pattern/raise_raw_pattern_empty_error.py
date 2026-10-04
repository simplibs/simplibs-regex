from typing import NoReturn
from simplibs.exception import ValidationError


def raise_raw_pattern_empty_error() -> NoReturn:
    """Raise a structured ValidationError when raw pattern text is empty."""
    raise ValidationError(
        error_name="RAW_PATTERN_EMPTY",
        label="text",
        value="",
        problem=(
            "Raw pattern text cannot be an empty string.",
            "An empty raw fragment has no meaningful syntax to insert into a regular expression pattern.",
        ),
        expected="A non-empty string of raw regex syntax (e.g., 'a{2,4}').",
        how_to_fix=(
            "Provide a non-empty string containing valid regex syntax.",
            "Example: RawPattern(r'a{2,4}')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_raw_pattern_empty_error — Empty Raw Pattern Guard

## Purpose
Guards RawPattern against being initialized with an empty string, ensuring every raw fragment carries actual syntax.
"""