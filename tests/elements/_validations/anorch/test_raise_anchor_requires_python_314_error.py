import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_anchor_requires_python_314_error,
)


def test_raise_anchor_requires_python_314_error_contract(subtests) -> None:
    """Verify that raise_anchor_requires_python_314_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_anchor_requires_python_314_error,
        invalid_params=(),
        exception_type=ValidationError,
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
        verbose=False,
    )