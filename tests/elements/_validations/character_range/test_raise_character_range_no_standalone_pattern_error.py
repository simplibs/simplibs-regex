"""
Tests for raise_character_range_no_standalone_pattern_error — validation of standalone character range.
"""
import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_range_no_standalone_pattern_error,
)


def test_raise_character_range_no_standalone_pattern_error_contract(subtests) -> None:
    """Verify that raise_character_range_no_standalone_pattern_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_character_range_no_standalone_pattern_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="CHARACTER_RANGE_NO_STANDALONE_PATTERN",
        label="CharacterRange",
        value="CharacterRange",
        problem=(
            "CharacterRange cannot be compiled as a standalone pattern.",
            "A character range (like 'a-z') only has meaning inside a CharacterClass `[...]`.",
        ),
        expected="CharacterRange nested within a CharacterClass.",
        how_to_fix=(
            "Wrap the CharacterRange inside a CharacterClass.",
            "Example: CharacterClass(CharacterRange('a', 'z'))",
        ),
        exception=ValueError,
        verbose=False,
    )