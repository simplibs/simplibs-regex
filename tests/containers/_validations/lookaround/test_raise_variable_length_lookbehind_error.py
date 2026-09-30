"""
Tests for raise_variable_length_lookbehind_error — validation of fixed-length lookbehinds.
"""
import pytest

from simplibs.regex.containers._validations import (
    raise_variable_length_lookbehind_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("variable_inner", ["Repeat(DIGIT, min=0, max=None)", "Alternation(Literal('a'), Repeat(Literal('b'), 1, 3))"])
def test_raise_variable_length_lookbehind_error(subtests, variable_inner):
    """Verify that variable-length inner nodes in lookbehinds raise a structured ValidationError."""
    assert_exception_function(
        subtests,
        raise_variable_length_lookbehind_error,
        invalid_params=(variable_inner,),
        exception_type=ValidationError,
        value=repr(variable_inner),
        label="Lookbehind inner node",
        expected="An inner regex node that yields a constant fixed length.",
        problem="requires `inner` to have a fixed length",
        how_to_fix="Ensure that every branch of an inner Alternation or Repeat",
        exception=ValueError,
        verbose=False
    )