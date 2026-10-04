from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_ascii_unicode_conflict_error() -> NoReturn:
    """Raise a structured ValidationError when both ASCII and UNICODE flags are specified."""
    raise ValidationError(
        error_name="GROUP_ASCII_UNICODE_CONFLICT",
        label="flags",
        value="ASCII, UNICODE",
        problem=(
            "`Flag.ASCII` and `Flag.UNICODE` cannot both be active simultaneously in a group.",
            "Python's regex engine treats ASCII and UNICODE character matching modes as mutually exclusive.",
        ),
        expected="Only one character-encoding flag (ASCII or UNICODE) per group.",
        how_to_fix=(
            "Keep either Flag.ASCII or Flag.UNICODE in `flags`, but not both.",
            "Example: Group(inner, flags={Flag.ASCII})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_group_ascii_unicode_conflict_error — ASCII and UNICODE Conflict Guard

## Purpose
Guards Group against specifying both ASCII and UNICODE encoding flags at the same time.
"""