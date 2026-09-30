from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_char_code_invalid_kind_error(kind: Any) -> NoReturn:
    """Raise a structured ParamError when CharCode() receives an invalid kind type."""
    raise ParamError(
        error_name="CHAR_CODE_INVALID_KIND",
        label="CharCode kind",
        value=type(kind).__name__,
        problem=(
            f"CharCode() requires a CharCodeKind, got {kind!r} of type '{type(kind).__name__}'.",
            "The kind parameter must be a valid member of the CharCodeKind enumeration.",
        ),
        expected="A CharCodeKind instance (e.g. CharCodeKind.HEX).",
        how_to_fix=(
            "Pass an explicit CharCodeKind enum value.",
        ),
        exception=TypeError,
    )