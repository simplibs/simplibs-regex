from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_param_invalid_type_error(
    param_name: str,
    expected: str,
    value: Any,
    example: str | None = None,
) -> NoReturn:
    """Raise a ParamError when a constructor argument has the wrong type.

    One shared guard for every plain type check (Regex node, bool, str, enum
    member, ...), so elements do not need one function per parameter.

    Args:
        param_name: The name of the parameter being validated (e.g., "text", "kind").
        expected: Human-readable description of the accepted type, phrased so it
            reads after "Pass" (e.g., "a Regex instance", "a bool").
        value: The invalid value received.
        example: Optional one-line usage example shown in the fix hints.

    Raises:
        ParamError: Always.
    """
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
"must be of this type". The caller supplies the parameter name, a readable
description of the accepted type and, optionally, an example — so adding a
new parameter never needs a new error function. Rules beyond the type
(ranges, identifiers, mutually exclusive options) keep their own dedicated
functions, because their messages are specific.
"""
