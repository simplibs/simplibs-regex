from typing import NoReturn
from simplibs.exception import ValidationError


def raise_conditional_invalid_name_error(id_or_name: str) -> NoReturn:
    """Raise a structured ValidationError when Conditional() name is not a valid identifier."""
    raise ValidationError(
        error_name="CONDITIONAL_INVALID_NAME_IDENTIFIER",
        label="Conditional id_or_name",
        value=id_or_name,
        problem=(
            f"Conditional() name must be a valid identifier, got {id_or_name!r}.",
            "Named group references in conditional patterns must follow standard identifier naming rules.",
        ),
        expected="A valid Python identifier string.",
        how_to_fix=(
            "Ensure the group name contains only alphanumeric characters and underscores.",
        ),
        exception=ValueError,
    )