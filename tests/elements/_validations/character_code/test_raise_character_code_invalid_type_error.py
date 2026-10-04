import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements.enums import CharacterCodeKind
from simplibs.regex.elements._validations import raise_character_code_invalid_type_error


def test_raise_character_code_invalid_type_error_contract(subtests) -> None:
    kind = CharacterCodeKind.HEX
    invalid_value = True
    assert_exception_function(
        subtests,
        raise_character_code_invalid_type_error,
        invalid_params=(kind, invalid_value),
        exception_type=ValidationError,
        error_name="CHAR_CODE_INVALID_TYPE",
        label="value",
        value=invalid_value,
        problem=(
            f"Invalid value type for character code kind '{kind.name}': received {invalid_value!r} (type bool).",
            "Booleans and non-integer types are not permitted as numeric character codes.",
        ),
        expected="An integer value within the valid range for the specified character code kind.",
        how_to_fix=(
            "Provide an integer value instead of a boolean or other type.",
            "Example: CharacterCode(CharacterCodeKind.HEX, 0x41)",
        ),
        exception=TypeError,
        verbose=False,
    )