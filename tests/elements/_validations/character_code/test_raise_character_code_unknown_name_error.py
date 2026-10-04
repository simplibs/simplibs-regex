import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_code_unknown_name_error,
)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "NOPE",
        "not a name",
        "KATAKANA LETTER AINU P",
    ],
)
def test_raise_character_code_unknown_name_error_contract(
    subtests,
    invalid_name,
) -> None:
    """Verify that raise_character_code_unknown_name_error raises ParamError
    wrapping ValueError when a NAMED character code is not a single-character Unicode name."""

    assert_exception_function(
        subtests,
        raise_character_code_unknown_name_error,
        invalid_params=(invalid_name,),
        exception_type=ParamError,
        error_name="CHARACTER_CODE_UNKNOWN_NAME_ERROR",
        label="value",
        expected="an official Unicode character name that denotes exactly one character",
        value=invalid_name,
        problem=(
            f"Unicode has no single character named {invalid_name!r}.",
            "Names are looked up exactly like \\N{...} in Python's re (case-insensitive, aliases such as 'LINE FEED' are accepted).",
        ),
        how_to_fix=(
            "Check the spelling of the name.",
            "Example: CharacterCode(CharacterCodeKind.NAMED, 'BULLET') or 'LATIN SMALL LETTER A'",
        ),
        exception=ValueError,
        verbose=False,
    )
