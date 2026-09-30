"""
Tests for raise_char_class_item_not_allowed_error.
"""
import pytest
from simplibs.regex.elements._validations import (
    raise_char_class_item_not_allowed_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_item", ["raw_string", 123, None, object()])
def test_raise_char_class_item_not_allowed_error(subtests, invalid_item):
    """Verify that a disallowed item raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_char_class_item_not_allowed_error,
        invalid_params=(invalid_item,),
        exception_type=ParamError,
        value=type(invalid_item).__name__,
        label="CharacterClass item",
        expected="A valid character class item",
        problem="which is not allowed",
        how_to_fix="Ensure all items passed to CharacterClass support character class contexts",
        exception=TypeError,
        verbose=False
    )