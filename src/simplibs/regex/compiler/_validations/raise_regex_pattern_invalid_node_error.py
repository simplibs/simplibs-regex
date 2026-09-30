from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_regex_pattern_invalid_node_error(node: Any) -> NoReturn:
    """Raise a structured ParamError when RegexPattern() receives an invalid node type."""
    raise ParamError(
        error_name="REGEX_PATTERN_INVALID_NODE",
        label="RegexPattern node",
        value=type(node).__name__,
        problem=(
            f"RegexPattern() requires a Regex instance for `node`, got {node!r} of type '{type(node).__name__}'.",
            "The node parameter must be an instance of the Regex base class.",
        ),
        expected="A Regex instance.",
        how_to_fix=(
            "Pass a valid composed Regex tree node to RegexPattern.",
        ),
        exception=TypeError,
    )