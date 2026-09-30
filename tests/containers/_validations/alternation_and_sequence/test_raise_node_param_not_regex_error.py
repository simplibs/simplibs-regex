"""
Tests for raise_requires_at_least_one_node_error — validation of non-empty container nodes.
"""
import pytest

from simplibs.regex.containers._validations import (
    raise_requires_at_least_one_node_error,
)
from simplibs.exception.exceptions import ValidationError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("container_name", ["Alternation", "Sequence"])
def test_raise_requires_at_least_one_node_error(subtests, container_name):
    """Verify that constructing containers with zero nodes raises a structured ValidationError."""
    assert_exception_function(
        subtests,
        raise_requires_at_least_one_node_error,
        invalid_params=(container_name,),
        exception_type=ValidationError,
        value=0,
        label=f"{container_name} nodes",
        expected="At least one valid Regex instance passed as a positional argument.",
        problem="requires at least one node — got none",
        how_to_fix="Pass one or more Regex nodes into",
        exception=ValueError,
        verbose=False
    )