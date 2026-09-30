"""
Tests for raise_node_param_not_regex_error — validation that container children are Regex nodes.
"""
import pytest

from simplibs.regex.containers._validations import (
    raise_node_param_not_regex_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_node", ["raw_string", 123, None, object()])
def test_raise_node_param_not_regex_error(subtests, invalid_node):
    """Verify that passing non-Regex items to containers raises a structured ParamError."""
    assert_exception_function(
        subtests,
        raise_node_param_not_regex_error,
        invalid_params=("Alternation", invalid_node),
        exception_type=ParamError,
        value=type(invalid_node).__name__,
        label="Alternation node",
        expected="A valid Regex node instance (e.g. Literal(...), Anchor, or another container).",
        problem="which is not a Regex instance",
        how_to_fix="Wrap raw strings or objects into appropriate atom classes",
        exception=TypeError,
        verbose=False
    )