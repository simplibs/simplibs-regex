import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_class_empty_error,
)


def test_raise_character_class_empty_error_contract(subtests) -> None:
    """Verify that raise_character_class_empty_error raises ValidationError wrapping ValueError."""
    assert_exception_function(
        subtests,
        raise_character_class_empty_error,
        invalid_params=(),
        exception_type=ValidationError,
        error_name="CHAR_CLASS_EMPTY",
        label="items",
        value="()",
        problem=(
            "A character class (`[...]`) cannot be empty.",
            "Python's regex engine requires at least one character or item inside a character class.",
        ),
        expected="At least one valid regex item (e.g., Literal, CharacterType, CharacterRange).",
        how_to_fix=(
            "Provide one or more items to include in the character class.",
            "Example: CharacterClass(Literal('a'), Literal('b'))",
        ),
        exception=ValueError,
        verbose=False,
    )