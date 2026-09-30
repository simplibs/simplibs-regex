from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_invalid_group_name_error(name: Any) -> NoReturn:
    """Raise a structured ParamError when `name` is not a valid Python-identifier-like group name."""
    raise ParamError(
        error_name="INVALID_GROUP_NAME",
        label="group name",
        value=name,
        problem=(
            f"Received group name {name!r}, which is not a valid identifier.",
            "Named capture groups in regular expressions must follow standard identifier naming rules.",
        ),
        expected="A non-empty string that forms a valid Python identifier (alphanumeric and underscores, not starting with a digit).",
        how_to_fix=(
            "Provide a valid string identifier for the group name (e.g., 'year', 'user_id').",
            "Ensure the name does not contain spaces, hyphens, or special characters.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_group_name_error — Group Name Validation

## Purpose
Provides a structured `ParamError` when a non-identifier or non-string value is passed
to `Group(..., name=...)`, ensuring valid regex group naming constraints.

## Integration
- **Caller**: `Group.__init__` check for `name`.
"""