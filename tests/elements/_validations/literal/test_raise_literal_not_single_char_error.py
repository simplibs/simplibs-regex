import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_literal_not_single_char_error


def test_raise_literal_not_single_char_error_contract(subtests) -> None:
    """Verify that raise_literal_not_single_char_error raises ValidationError wrapping ValueError."""
    invalid_text = "ab"

    assert_exception_function(
        subtests,
        raise_literal_not_single_char_error,
        invalid_params=(invalid_text,),
        exception_type=ValidationError,
        error_name="LITERAL_NOT_SINGLE_CHAR",
        label="text",
        value=invalid_text,
        problem=(
            f"Literal text '{invalid_text}' has length {len(invalid_text)}, but character classes require single-character fragments.",
            "Multi-character literals cannot be rendered directly inside character class brackets (`[...]`).",
        ),
        expected="A single-character literal (e.g., Literal('a')).",
        how_to_fix=(
            "Ensure the literal contains only one character when used inside a CharacterClass.",
            "Example: CharacterClass(Literal('a'))",
        ),
        exception=ValueError,
        verbose=False,
    )