import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_multi_character_literal_in_char_class_error,
)


def test_raise_multi_character_literal_in_char_class_error_contract(subtests) -> None:
    """Verify that raise_multi_character_literal_in_char_class_error raises ValidationError wrapping ValueError."""
    invalid_text = "abc"

    assert_exception_function(
        subtests,
        raise_multi_character_literal_in_char_class_error,
        invalid_params=(invalid_text,),
        exception_type=ValidationError,
        error_name="MULTI_CHAR_LITERAL_IN_CHAR_CLASS",
        label="items",
        value=invalid_text,
        problem=(
            f"Literal text '{invalid_text}' has length {len(invalid_text)}, but character classes only accept single-character literals.",
            "A character class matches a single character from a set; multi-character strings cannot be direct members.",
        ),
        expected="A single-character Literal (e.g., Literal('a')).",
        how_to_fix=(
            "Pass single-character Literals or split the string into individual characters.",
            "Example: CharacterClass(Literal('a'), Literal('b'))",
        ),
        exception=ValueError,
        verbose=False,
    )