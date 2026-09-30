"""
Tests for raise_regex_pattern_invalid_node_error.
"""
import pytest
from simplibs.regex.compiler._validations.raise_regex_pattern_invalid_node_error import (
    raise_regex_pattern_invalid_node_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_node", ["not_a_node", 123, None])
def test_raise_regex_pattern_invalid_node_error(subtests, invalid_node):
    """Verify that an invalid node type raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_regex_pattern_invalid_node_error,
        invalid_params=(invalid_node,),
        exception_type=ParamError,
        value=type(invalid_node).__name__,
        label="RegexPattern node",
        expected="A Regex instance.",
        problem="requires a Regex instance for `node`",
        how_to_fix="Pass a valid composed Regex tree node to RegexPattern",
        exception=TypeError,
        verbose=False
    )