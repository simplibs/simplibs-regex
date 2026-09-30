from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_anchor_invalid_kind_error(kind: Any) -> NoReturn:
    """Raise a structured ParamError when Anchor() receives an invalid kind type."""
    raise ParamError(
        error_name="ANCHOR_INVALID_KIND",
        label="Anchor kind",
        value=type(kind).__name__,
        problem=(
            f"Anchor() requires an AnchorKind, got {kind!r} of type '{type(kind).__name__}'.",
            "The kind parameter must be a valid member of the AnchorKind enumeration.",
        ),
        expected="An AnchorKind instance (e.g. AnchorKind.START, AnchorKind.END).",
        how_to_fix=(
            "Pass an explicit AnchorKind enum value.",
        ),
        exception=TypeError,
    )