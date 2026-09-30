from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_flags_off_without_flags_error() -> NoReturn:
    """Raise a structured ValidationError when flags_off is given without explicit flags."""
    raise ValidationError(
        error_name="GROUP_FLAGS_OFF_WITHOUT_FLAGS",
        label="Group modifiers",
        value="flags_off without flags",
        problem=(
            "`flags_off` was given without `flags` — pass the flags that stay ON explicitly, even if empty via `flags=frozenset()`.",
            "Implicit flag states are disallowed to ensure call-site readability.",
        ),
        expected="Explicit `flags` parameter accompanying `flags_off`.",
        how_to_fix=(
            "Provide `flags=frozenset()` or active flags alongside `flags_off`.",
        ),
        exception=ValueError,
    )