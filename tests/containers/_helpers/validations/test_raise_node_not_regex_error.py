import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._helpers.validations import (
    raise_node_not_regex_error,
)


@pytest.mark.parametrize(
    "caller_name, invalid_node",
    [
        ("Alternation", "not_a_regex"),
        ("Alternation", 123),
        ("Sequence", None),
        ("Sequence", ["some_list"]),
    ],
)
def test_raise_node_not_regex_error_contract(
    subtests,
    caller_name,
    invalid_node,
) -> None:
    """Verify that raise_node_not_regex_error raises ParamError
    wrapping TypeError when a non-Regex node is passed to a container."""

    received_type = type(invalid_node).__name__

    assert_exception_function(
        subtests,
        raise_node_not_regex_error,
        invalid_params=(caller_name, invalid_node),
        exception_type=ParamError,
        error_name="NODE_NOT_REGEX_ERROR",
        label="nodes",
        expected="a Regex instance",
        value=invalid_node,
        problem=(
            f"Container {caller_name}() received an invalid item that is not a Regex node.",
            f"Received type '{received_type}' with value: {invalid_node!r}.",
        ),
        how_to_fix=(
            f"Ensure all arguments passed to {caller_name}() inherit from Regex.",
            "Use Regex building blocks (like Literal, DIGIT, Group) for container items.",
        ),
        exception=TypeError,
        verbose=False,
    )