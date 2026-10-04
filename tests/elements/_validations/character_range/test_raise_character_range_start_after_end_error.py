import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_range_start_after_end_error,
)


def test_raise_character_range_start_after_end_error_contract(subtests) -> None:
    """Verify that raise_character_range_start_after_end_error raises ValidationError wrapping ValueError."""
    start = "z"
    end = "a"

    assert_exception_function(
        subtests,
        raise_character_range_start_after_end_error,
        invalid_params=(start, end),
        exception_type=ValidationError,
        error_name="CHARACTER_RANGE_START_AFTER_END",
        label="start/end",
        value=f"{start}-{end}",
        problem=(
            f"Character range start ('{start}', ord={ord(start)}) cannot come after end ('{end}', ord={ord(end)}).",
            "The starting character of a range must have a lower or equal ASCII/Unicode code point than the ending character.",
        ),
        expected="A valid ascending range (start <= end).",
        how_to_fix=(
            "Swap the start and end characters so they form an ascending range.",
            f"Example: CharacterRange('{end}', '{start}')",
        ),
        exception=ValueError,
        verbose=False,
    )