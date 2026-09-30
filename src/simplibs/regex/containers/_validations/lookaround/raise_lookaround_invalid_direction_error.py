from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_lookaround_invalid_direction_error(direction: Any) -> NoReturn:
    """Raise a structured ParamError when Lookaround() receives an invalid direction type."""
    raise ParamError(
        error_name="LOOKAROUND_INVALID_DIRECTION",
        label="Lookaround direction",
        value=type(direction).__name__,
        problem=(
            f"Lookaround() requires a LookaroundDirection for `direction`, got {direction!r} of type '{type(direction).__name__}'.",
            "The direction parameter must be a valid member of the LookaroundDirection enumeration.",
        ),
        expected="A LookaroundDirection instance (e.g. LookaroundDirection.AHEAD or LookaroundDirection.BEHIND).",
        how_to_fix=(
            "Pass an explicit LookaroundDirection enum value.",
        ),
        exception=TypeError,
    )