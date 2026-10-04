import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_character_code_invalid_named_value_error


def test_raise_character_code_invalid_named_value_error_contract(subtests) -> None:
    invalid_value = ""
    assert_exception_function(
        subtests,
        raise_character_code_invalid_named_value_error,
        invalid_params=(invalid_value,),
        exception_type=ValidationError,
        error_name="CHAR_CODE_INVALID_NAMED_VALUE",
        label="value",
        value=invalid_value,
        problem=(
            f"Invalid named character code value: {invalid_value!r}.",
            "Named character escapes (`\\N{NAME}`) require a non-empty Unicode character name string.",
        ),
        expected="A non-empty string representing a Unicode character name.",
        how_to_fix=(
            "Provide a valid non-empty string for the character name.",
            "Example: CharacterCode(CharacterCodeKind.NAMED, 'BULLET')",
        ),
        exception=ValueError,
        verbose=False,
    )