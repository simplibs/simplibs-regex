import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_class_item_not_allowed_error,
)


def test_raise_character_class_item_not_allowed_error_contract(subtests) -> None:
    """Verify that raise_character_class_item_not_allowed_error raises ValidationError wrapping TypeError."""
    invalid_item = "not_a_regex"
    received_type = "str"

    assert_exception_function(
        subtests,
        raise_character_class_item_not_allowed_error,
        invalid_params=(invalid_item,),
        exception_type=ValidationError,
        error_name="CHAR_CLASS_ITEM_NOT_ALLOWED",
        label="items",
        value=invalid_item,
        problem=(
            f"Item of type '{received_type}' with value {invalid_item!r} is not allowed inside a character class.",
            "Only specific regex elements opted into character class usage (`_usable_in_char_class = True`) are permitted.",
        ),
        expected="A valid character class item (Literal, CharacterType, CharacterRange, or CharacterCode).",
        how_to_fix=(
            "Ensure all items passed to CharacterClass are supported inside character classes.",
            "Example: CharacterClass(DIGIT, Literal('a'))",
        ),
        exception=TypeError,
        verbose=False,
    )