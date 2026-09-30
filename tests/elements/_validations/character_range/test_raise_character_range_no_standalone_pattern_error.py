"""
Tests for raise_character_range_no_standalone_pattern_error.
"""
from simplibs.regex.elements._validations import (
    raise_character_range_no_standalone_pattern_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


def test_raise_character_range_no_standalone_pattern_error(subtests):
    """Verify that calling to_pattern on CharacterRange raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_character_range_no_standalone_pattern_error,
        invalid_params=(),
        exception_type=ParamError,
        value="standalone",
        label="CharacterRange pattern",
        expected="Embedding inside a CharacterClass.",
        problem="CharacterRange has no standalone pattern",
        how_to_fix="Wrap the CharacterRange inside CharacterClass",
        exception=TypeError,
        verbose=False
    )