from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_group_inner_not_regex_error(inner: Any) -> NoReturn:
    """Raise a structured ParamError when Group() inner is not a Regex instance."""
    raise ParamError(
        error_name="GROUP_INNER_NOT_REGEX",
        label="Group inner",
        value=type(inner).__name__,
        problem=(
            f"Group() requires a Regex instance for `inner`, got {inner!r} of type '{type(inner).__name__}'.",
            "The inner component of a group must be a valid regex node.",
        ),
        expected="A valid Regex instance.",
        how_to_fix=(
            "Wrap raw strings or objects into appropriate atom classes (like Literal(...)).",
        ),
        exception=TypeError,
    )