from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_conditional_invalid_id_type_error(
    id_or_name: Any
) -> NoReturn:
    """Raise a ParamError when a conditional group ID or name is of an invalid type
    (such as a boolean or unsupported type).

    Args:
        id_or_name: The invalid value received for the conditional reference.

    Raises:
        ParamError: Always.
    """
    received_type = type(id_or_name).__name__

    raise ParamError(
        error_name="CONDITIONAL_INVALID_ID_TYPE_ERROR",
        label="id_or_name",
        expected="an integer (>= 1) or a string identifier",
        value=id_or_name,
        problem=(
            f"Conditional group reference received an invalid type '{received_type}' with value {id_or_name!r}.",
            "Booleans and other non-int/non-str types are not valid group references.",
        ),
        how_to_fix=(
            "Provide either a positive integer group number or a string group identifier.",
            "Example: Conditional(1, Literal('yes'), Literal('no')) or Conditional('group_name', Literal('yes'))",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_conditional_invalid_id_type_error — Conditional ID Type Guard

## Purpose
Guards Conditional against unsupported types passed as group references (such as booleans
which inherit from int, or arbitrary objects), ensuring clean failure with a TypeError wrapper.
"""