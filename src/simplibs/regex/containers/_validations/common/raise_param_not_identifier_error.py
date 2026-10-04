from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_param_not_identifier_error(
    param_name: str,
    value: Any
) -> NoReturn:
    """Raise a ParamError when a string parameter that must be a valid
    Python identifier fails the isidentifier() check.

    Args:
        param_name: The name of the parameter being validated (e.g., "name", "id_or_name").
        value: The invalid value received.

    Raises:
        ParamError: Always.
    """
    raise ParamError(
        error_name="PARAM_NOT_IDENTIFIER_ERROR",
        label=param_name,
        expected="a valid Python identifier string",
        value=value,
        problem=(
            f"Parameter '{param_name}' received value {value!r}, which is not a valid identifier.",
            "Identifiers must consist of alphanumeric characters and underscores, and cannot start with a digit.",
        ),
        how_to_fix=(
            f"Provide a valid Python identifier string for parameter '{param_name}'.",
            "Example: use alphanumeric characters and underscores (e.g., 'my_group', 'target1').",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_param_not_identifier_error — Shared Identifier Guard

## Purpose
Centralizes validation error reporting for string parameters across containers
(such as Group and Conditional) that require valid Python identifier names.
"""