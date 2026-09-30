from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_character_range_invalid_boundary_error(name: str, value: Any) -> NoReturn:
    """Raise a structured ParamError when CharacterRange boundary is not a single character."""
    raise ParamError(
        error_name="CHARACTER_RANGE_INVALID_BOUNDARY",
        label=f"CharacterRange {name}",
        value=repr(value),
        problem=(
            f"CharacterRange() requires `{name}` to be a single character, got {value!r}.",
            "Range boundaries must be exact single-character strings.",
        ),
        expected="A single-character string (len == 1).",
        how_to_fix=(
            "Provide a single character for both `start` and `end` boundaries.",
        ),
        exception=ValueError,
    )