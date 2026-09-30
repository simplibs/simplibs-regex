from typing import NoReturn
from simplibs.exception import ParamError


def raise_group_reference_invalid_identifier_error(id_or_name: str) -> NoReturn:
    """Raise a structured ParamError when GroupReference name is not a valid identifier."""
    raise ParamError(
        error_name="GROUP_REFERENCE_INVALID_IDENTIFIER",
        label="GroupReference name",
        value=repr(id_or_name),
        problem=(
            f"GroupReference() name must be a valid identifier, got {id_or_name!r}.",
            "Named group references must follow standard Python identifier naming rules.",
        ),
        expected="A valid Python identifier string.",
        how_to_fix=(
            "Provide a valid identifier string for the group name.",
        ),
        exception=ValueError,
    )