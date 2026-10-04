from typing import NoReturn
from simplibs.exception import ParamError


def raise_no_nodes_error(
    caller_name: str
) -> NoReturn:
    """Raise a ParamError when a container constructor is called with zero nodes.

    Args:
        caller_name: Name of the container raising the error (e.g. "Alternation", "Sequence").

    Raises:
        ParamError: Always.
    """
    raise ParamError(
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
    )


_DESIGN_NOTES = """
# raise_no_nodes_error — Container Empty Input Guard

## Purpose
Guards container constructors (Alternation, Sequence, etc.) against empty inputs,
failing fast with a clear diagnostic message naming the offending container.
"""