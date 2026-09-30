from typing import NoReturn
from simplibs.exception import ParamError


def raise_literal_empty_error() -> NoReturn:
    """Raise a structured ParamError when Literal() receives an empty string."""
    raise ParamError(
        error_name="LITERAL_EMPTY",
        label="Literal text",
        value="''",
        problem=(
            "Literal() requires a non-empty string.",
            "An empty literal matches nothing meaningful in this DSL.",
        ),
        expected="A non-string with len >= 1.",
        how_to_fix=(
            "Provide a non-empty string for the Literal.",
        ),
        exception=ValueError,
    )