import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_raw_pattern_empty_error


def test_raise_raw_pattern_empty_error_contract(subtests) -> None:
    """Verify that raise_raw_pattern_empty_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_raw_pattern_empty_error,
        invalid_params=(),
        exception_type=ValidationError,
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
        verbose=False,
    )