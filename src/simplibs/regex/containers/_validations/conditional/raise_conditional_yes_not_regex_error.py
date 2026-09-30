from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_conditional_yes_not_regex_error(yes: Any) -> NoReturn:
    """Raise a structured ParamError when the yes branch is not a Regex instance."""
    raise ParamError(
        error_name="CONDITIONAL_YES_NOT_REGEX",
        label="Conditional yes",
        value=type(yes).__name__,
        problem=(
            f"Conditional() requires a Regex instance for `yes`, got {yes!r} of type '{type(yes).__name__}'.",
            "The 'yes' branch of a conditional expression must be a valid regex component.",
        ),
        expected="A valid Regex instance.",
        how_to_fix=(
            "Wrap raw strings or objects into appropriate atom classes (like Literal(...)).",
        ),
        exception=TypeError,
    )