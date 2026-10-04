import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements.enums import CharacterCodeKind
from simplibs.regex.elements._validations import raise_character_code_out_of_range_error


def test_raise_character_code_out_of_range_error_contract(subtests) -> None:
    kind = CharacterCodeKind.HEX
    invalid_value = 300
    low, high = 0x00, 0xFF

    assert_exception_function(
        subtests,
        raise_character_code_out_of_range_error,
        invalid_params=(kind, invalid_value, low, high),
        exception_type=ValidationError,
        error_name="CHAR_CODE_OUT_OF_RANGE",
        label="value",
        value=invalid_value,
        problem=(
            f"Character code value {invalid_value} (0x{invalid_value:x}) is out of range for kind '{kind.name}'.",
            f"Allowed range for this kind is between {low} (0x{low:x}) and {high} (0x{high:x}).",
        ),
        expected=f"An integer between {low} and {high}.",
        how_to_fix=(
            f"Provide a value that fits within the valid range for {kind.name}.",
            f"Example: CharacterCode(CharacterCodeKind.{kind.name}, {low})",
        ),
        exception=ValueError,
        verbose=False,
    )