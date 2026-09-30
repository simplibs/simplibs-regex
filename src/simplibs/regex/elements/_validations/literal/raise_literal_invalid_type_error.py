from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_literal_invalid_type_error(text: Any) -> NoReturn:
    """Raise a structured ParamError when Literal() receives a non-string type."""
    raise ParamError(
        error_name="LITERAL_INVALID_TYPE",
        label="Literal text",
        value=type(text).__name__,
        problem=(
            f"Literal() requires a str, got {text!r} of type '{type(text).__name__}'.",
            "Literal text must be specified using a string value.",
        ),
        expected="A string value.",
        how_to_fix=(
            "Pass a string to the Literal constructor.",
        ),
        exception=TypeError,
    )