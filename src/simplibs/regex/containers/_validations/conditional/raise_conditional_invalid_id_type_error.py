from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_conditional_invalid_id_type_error(id_or_name: Any) -> NoReturn:
    """Raise a structured ParamError when Conditional() receives an unsupported type for id_or_name."""
    raise ParamError(
        error_name="CONDITIONAL_INVALID_ID_TYPE",
        label="Conditional id_or_name",
        value=type(id_or_name).__name__,
        problem=(
            f"Conditional() requires an int or str for `id_or_name`, got {id_or_name!r} of type '{type(id_or_name).__name__}'.",
            "Conditional group references must be referenced by numeric ID or name string.",
        ),
        expected="An int or str instance.",
        how_to_fix=(
            "Pass an integer group index or a string group name as the first argument.",
        ),
        exception=TypeError,
    )