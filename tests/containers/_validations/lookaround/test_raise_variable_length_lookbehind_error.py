"""
Tests for raise_variable_length_lookbehind_error — validation of fixed-length lookbehinds.
"""
import pytest

from simplibs.regex.containers._validations import (
    raise_variable_length_lookbehind_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize(
    "variable_inner",
    [
        "Repeat(DIGIT, min=0, max=None)",
        "Alternation(Literal('a'), Repeat(Literal('b'), 1, 3))",
    ],
)
def test_raise_variable_length_lookbehind_error(subtests, variable_inner):
    """Verify that variable-length inner nodes in lookbehinds raise a structured ValidationError."""
    assert_exception_function(
        subtests,
        raise_variable_length_lookbehind_error,
        invalid_params=(variable_inner,),
        exception_type=ValidationError,
        value=variable_inner,
        label="inner",
        expected="An inner regex pattern with a fixed length.",
        problem="Lookbehind assertions",
        how_to_fix="Ensure the inner pattern uses only fixed-length components",
        exception=ValueError,
        verbose=False,
    )