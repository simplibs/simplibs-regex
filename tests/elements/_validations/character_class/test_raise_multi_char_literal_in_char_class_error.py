"""
Tests for raise_multi_char_literal_in_char_class_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_multi_char_literal_in_char_class_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_text", ["ab", "abc", "hello", "123"])
def test_raise_multi_char_literal_in_char_class_error(subtests, invalid_text):
    """Verify that a multi-character literal raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_multi_char_literal_in_char_class_error,
        invalid_params=(invalid_text,),
        exception_type=ParamError,
        value=invalid_text,
        label="CharacterClass literal",
        expected="A single-character Literal (len == 1).",
        problem="multi-character Literal",
        how_to_fix="Split multi-character strings into individual literals",
        exception=ValueError,
        verbose=False
    )