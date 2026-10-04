from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_reference_invalid_identifier_error(value: str) -> NoReturn:
    """Raise a structured ValidationError when named group reference is not a valid Python identifier."""
    raise ValidationError(
        error_name="GROUP_REFERENCE_INVALID_IDENTIFIER",
        label="id_or_name",
        value=value,
        problem=(
            f"Named group reference '{value}' is not a valid identifier.",
            "Group names must be valid Python identifiers (alphanumeric characters and underscores, not starting with a digit).",
        ),
        expected="A valid identifier string representing a named group.",
        how_to_fix=(
            "Provide a valid identifier string for the group name.",
            "Example: GroupReference('user_id')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_group_reference_invalid_identifier_error — Invalid Identifier Guard

## Purpose
Guards named group references against strings that do not conform to valid identifier naming rules.
"""