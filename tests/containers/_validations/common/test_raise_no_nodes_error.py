import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_no_nodes_error,
)


@pytest.mark.parametrize(
    "caller_name",
    [
        "Alternation",
        "Sequence",
    ],
)
def test_raise_no_nodes_error_contract(
    subtests,
    caller_name,
) -> None:
    """Verify that raise_no_nodes_error raises ParamError
    wrapping ValueError when a container is instantiated without nodes."""

    assert_exception_function(
        subtests,
        raise_no_nodes_error,
        invalid_params=(caller_name,),
        exception_type=ParamError,
        error_name="NO_NODES_ERROR",
        label="nodes",
        expected="at least one Regex node",
        value=None,
        problem=(
            f"Container {caller_name}() was called with zero nodes.",
            "At least one Regex instance is required to construct a valid container.",
        ),
        how_to_fix=(
            f"Provide one or more Regex nodes when instantiating {caller_name}().",
            f"Example: {caller_name}(Literal('a'), Literal('b'))",
        ),
        exception=ValueError,
        verbose=False,
    )