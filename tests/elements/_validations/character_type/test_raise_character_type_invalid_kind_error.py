"""
Tests for raise_character_type_invalid_kind_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_character_type_invalid_kind_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_kind", ["DIGIT", "\\d", 123, None])
def test_raise_character_type_invalid_kind_error(subtests, invalid_kind):
    """Verify that an invalid kind type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_character_type_invalid_kind_error,
        invalid_params=(invalid_kind,),
        exception_type=ParamError,
        value=type(invalid_kind).__name__,
        label="CharacterType kind",
        expected="A CharacterTypeKind instance",
        problem="requires a CharacterTypeKind",
        how_to_fix="Pass an explicit CharacterTypeKind enum value",
        exception=TypeError,
        verbose=False
    )