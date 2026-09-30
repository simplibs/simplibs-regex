from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_group_reference_invalid_type_error(id_or_name: Any) -> NoReturn:
    """Raise a structured ParamError when GroupReference receives a non-int, non-str type."""
    raise ParamError(
        error_name="GROUP_REFERENCE_INVALID_TYPE",
        label="GroupReference target",
        value=type(id_or_name).__name__,
        problem=(
            f"GroupReference() requires an int or str, got {id_or_name!r} of type '{type(id_or_name).__name__}'.",
            "Group references must be specified either by numeric position (int) or group name (str).",
        ),
        expected="An integer or string value.",
        how_to_fix=(
            "Pass an integer group number or a string group name.",
        ),
        exception=TypeError,
    )