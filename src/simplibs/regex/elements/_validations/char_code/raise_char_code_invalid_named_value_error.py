from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_char_code_invalid_named_value_error(value: Any) -> NoReturn:
    """Raise a structured ParamError when CharCode(NAMED, ...) receives an invalid value."""
    raise ParamError(
        error_name="CHAR_CODE_INVALID_NAMED_VALUE",
        label="CharCode named value",
        value=repr(value),
        problem=(
            f"CharCode(NAMED, ...) requires a non-empty str name, got {value!r}.",
            "Named character codes must be specified via a non-empty string.",
        ),
        expected="A non-empty string representing a Unicode character name.",
        how_to_fix=(
            "Provide a valid non-empty string name.",
        ),
        exception=ValueError,
    )