from typing import Any, NoReturn
from simplibs.exception import ParamError

# Internal metadata registry mapping parameter names to expected descriptions and examples
_PARAM_METADATA: dict[str, tuple[str, str | None]] = {
    "node": ("a Regex instance", None),
    "flags": ("a set or frozenset of Flag members", "frozenset({Flag.IGNORECASE})"),
    "description": ("a str", None),
    "lazy": ("a bool", None),
}


def raise_param_invalid_type_error(
    param_name: str,
    value: Any,
) -> NoReturn:
    """Raise a ParamError when a constructor argument has the wrong type.

    Looks up expected type descriptions and optional examples internally
    based on the parameter name.

    Args:
        param_name: The name of the parameter being validated (e.g., "node", "lazy").
        value: The invalid value received.

    Raises:
        ParamError: Always.
    """
    if param_name in _PARAM_METADATA:
        expected, example = _PARAM_METADATA[param_name]
    else:
        expected, example = f"a valid type for '{param_name}'", None

    received_type = type(value).__name__

    how_to_fix = [f"Pass {expected} for parameter '{param_name}'."]
    if example:
        how_to_fix.append(f"Example: {example}")

    raise ParamError(
        error_name="PARAM_INVALID_TYPE_ERROR",
        label=param_name,
        expected=expected,
        value=value,
        problem=(
            f"Parameter '{param_name}' received {value!r} of type '{received_type}'.",
            f"Expected {expected}.",
        ),
        how_to_fix=tuple(how_to_fix),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_param_invalid_type_error — Shared Parameter Type Guard

## Purpose
Single type-check error for every constructor parameter whose only rule is
"must be of this type". Uses an internal metadata registry so callers only
need to provide the parameter name and value.
"""