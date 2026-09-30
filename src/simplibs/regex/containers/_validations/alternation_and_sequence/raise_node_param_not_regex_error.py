from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_node_param_not_regex_error(container_name: str, value: Any) -> NoReturn:
    """Raise a structured ParamError when a container receives a non-Regex positional argument."""
    raise ParamError(
        error_name="CONTAINER_NODE_NOT_REGEX",
        label=f"{container_name} node",
        value=type(value).__name__,
        problem=(
            f"{container_name}() received {value!r} of type '{type(value).__name__}', which is not a Regex instance.",
            "All child elements within structural containers must inherit from the base Regex class.",
        ),
        expected="A valid Regex node instance (e.g. Literal(...), Anchor, or another container).",
        how_to_fix=(
            "Wrap raw strings or objects into appropriate atom classes (like Literal(...)).",
            "Ensure all arguments passed to the container are valid regex components.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_node_param_not_regex_error — Container Child Type Validation

## Purpose
Provides a standardized `ParamError` when invalid (non-`Regex`) objects are passed 
as children to structural containers like `Alternation` or `Sequence`.
"""