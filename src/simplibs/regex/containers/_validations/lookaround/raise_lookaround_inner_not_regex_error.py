from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_lookaround_inner_not_regex_error(inner: Any) -> NoReturn:
    """Raise a structured ParamError when Lookaround() inner is not a Regex instance."""
    raise ParamError(
        error_name="LOOKAROUND_INNER_NOT_REGEX",
        label="Lookaround inner",
        value=type(inner).__name__,
        problem=(
            f"Lookaround() requires a Regex instance for `inner`, got {inner!r} of type '{type(inner).__name__}'.",
            "The inner component of a lookaround assertion must be a valid regex node.",
        ),
        expected="A valid Regex instance.",
        how_to_fix=(
            "Wrap raw strings or objects into appropriate atom classes (like Literal(...)).",
        ),
        exception=TypeError,
    )