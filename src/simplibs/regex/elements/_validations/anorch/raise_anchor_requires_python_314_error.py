from typing import NoReturn
from simplibs.exception import ValidationError


def raise_anchor_requires_python_314_error() -> NoReturn:
    """Raise a structured ValidationError when AnchorKind.END_STRING_PY314 is used on Python < 3.14."""
    raise ValidationError(
        error_name="ANCHOR_REQUIRES_PYTHON_314",
        label="kind",
        value="AnchorKind.END_STRING_PY314",
        problem=(
            "`AnchorKind.END_STRING_PY314` (`\\z`) requires Python 3.14 or newer.",
            "The current Python interpreter version does not support the `\\z` anchor escape sequence.",
        ),
        expected="Python 3.14+ when using AnchorKind.END_STRING_PY314, or use AnchorKind.END_STRING (`\\Z`) for universal compatibility.",
        how_to_fix=(
            "Use `AnchorKind.END_STRING` (`\\Z`) instead, which has the identical meaning and works on all Python versions.",
            "Example: Anchor(AnchorKind.END_STRING)",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_anchor_requires_python_314_error — Python 3.14 Anchor Guard

## Purpose
Guards Anchor against using the `\\z` escape sequence on Python versions older than 3.14, offering a friendly suggestion to use `\\Z` instead.
"""