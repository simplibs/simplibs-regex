import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_literal_empty_error


def test_raise_literal_empty_error_contract(subtests) -> None:
    """Verify that raise_literal_empty_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_literal_empty_error,
        invalid_params=(),
        exception_type=ValidationError,
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
        verbose=False,
    )