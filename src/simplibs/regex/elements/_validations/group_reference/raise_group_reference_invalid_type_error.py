from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_group_reference_invalid_type_error(value: Any) -> NoReturn:
    """Raise a structured ValidationError when group reference type is invalid (e.g. bool)."""
    raise ValidationError(
        error_name="GROUP_REFERENCE_INVALID_TYPE",
        label="id_or_name",
        value=value,
        problem=(
            f"Invalid group reference type: received {value!r} (type {type(value).__name__}).",
            "Booleans and non-integer/non-string types are not permitted as group references.",
        ),
        expected="An integer group number (1-99) or a valid identifier string for a named group.",
        how_to_fix=(
            "Provide an integer or a string instead of a boolean or other type.",
            "Example: GroupReference(1) or GroupReference('year')",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_group_reference_invalid_type_error — Invalid Type Guard

## Purpose
Guards GroupReference against incorrect types such as booleans passed as integer group numbers.
"""