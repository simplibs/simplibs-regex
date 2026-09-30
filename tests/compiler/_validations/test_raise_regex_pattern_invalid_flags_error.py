"""
Tests for raise_regex_pattern_invalid_flags_error.
"""
import pytest
from simplibs.regex.compiler._validations.raise_regex_pattern_invalid_flags_error import (
    raise_regex_pattern_invalid_flags_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_flags", [["IGNORECASE"], frozenset(["IGNORECASE"]), 123])
def test_raise_regex_pattern_invalid_flags_error(subtests, invalid_flags):
    """Verify that invalid flags raise a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_regex_pattern_invalid_flags_error,
        invalid_params=(invalid_flags,),
        exception_type=ParamError,
        value=repr(invalid_flags),
        label="RegexPattern flags",
        expected="A frozenset of Flag members.",
        problem="requires `flags` to be a frozenset of Flag members",
        how_to_fix="Pass flags as a frozenset of Flag objects",
        exception=TypeError,
        verbose=False
    )