from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_conditional_no_not_regex_error(no: Any) -> NoReturn:
    """Raise a structured ParamError when the no branch is neither a Regex instance nor None."""
    raise ParamError(
        error_name="CONDITIONAL_NO_NOT_REGEX",
        label="Conditional no",
        value=type(no).__name__,
        problem=(
            f"Conditional() requires a Regex instance or None for `no`, got {no!r} of type '{type(no).__name__}'.",
            "The 'no' branch of a conditional expression must be a valid regex component or omitted.",
        ),
        expected="A valid Regex instance or None.",
        how_to_fix=(
            "Wrap raw strings or objects into appropriate atom classes (like Literal(...)) or omit the 'no' branch.",
        ),
        exception=TypeError,
    )