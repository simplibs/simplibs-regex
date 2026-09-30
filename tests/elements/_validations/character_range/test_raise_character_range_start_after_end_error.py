"""
Tests for raise_character_range_start_after_end_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_character_range_start_after_end_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("start, end", [("z", "a"), ("9", "0"), ("b", "a")])
def test_raise_character_range_start_after_end_error(subtests, start, end):
    """Verify that start > end raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_character_range_start_after_end_error,
        invalid_params=(start, end),
        exception_type=ParamError,
        value=f"start={start!r}, end={end!r}",
        label="CharacterRange bounds",
        expected="start <= end in character order.",
        problem="is invalid — `start` must not come after `end`",
        how_to_fix="Ensure `start` comes before or equals `end`",
        exception=ValueError,
        verbose=False
    )