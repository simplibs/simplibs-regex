from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_node_not_regex_error(
    caller_name: str,
    node: Any
) -> NoReturn:
    """Raise a ParamError when a node passed to a container constructor
    is not an instance of Regex.

    Args:
        caller_name: Name of the container raising the error (e.g. "Alternation", "Sequence").
        node: The invalid non-regex value received.

    Raises:
        ParamError: Always.
    """
    received_type = type(node).__name__

    raise ParamError(
        error_name="NODE_NOT_REGEX_ERROR",
        label="nodes",
        expected="a Regex instance",
        value=node,
        problem=(
            f"Container {caller_name}() received an invalid item that is not a Regex node.",
            f"Received type '{received_type}' with value: {node!r}.",
        ),
        how_to_fix=(
            f"Ensure all arguments passed to {caller_name}() inherit from Regex.",
            "Use Regex building blocks (like Literal, DIGIT, Group) for container items.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_node_not_regex_error — Container Node Type Guard

## Purpose
Guards container constructors (Alternation, Sequence, etc.) against non-Regex inputs,
providing clear diagnostic details naming the offending container and received value.
"""