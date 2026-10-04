import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_character_code_invalid_kind_error


def test_raise_character_code_invalid_kind_error_contract(subtests) -> None:
    invalid_kind = "invalid"
    assert_exception_function(
        subtests,
        raise_character_code_invalid_kind_error,
        invalid_params=(invalid_kind,),
        exception_type=ValidationError,
        error_name="CHAR_CODE_INVALID_KIND",
        label="kind",
        value=invalid_kind,
        problem=(
            f"Invalid character code kind: {invalid_kind!r}.",
            "The kind parameter must be a valid member of the `CharacterCodeKind` enum.",
        ),
        expected="A valid `CharacterCodeKind` instance (e.g., CharacterCodeKind.HEX).",
        how_to_fix=(
            "Provide a valid `CharacterCodeKind` enum member.",
            "Example: CharacterCode(CharacterCodeKind.HEX, 0x41)",
        ),
        exception=TypeError,
        verbose=False,
    )