from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_name_requires_capturing_error() -> NoReturn:
    """Raise a structured ValidationError when a named group has capturing=False."""
    raise ValidationError(
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
    )


_DESIGN_NOTES = """
# raise_group_name_requires_capturing_error — Name Requires Capturing Guard

## Purpose
Guards Group against disabling capturing on a named group, which is structurally impossible in Python regex.
"""