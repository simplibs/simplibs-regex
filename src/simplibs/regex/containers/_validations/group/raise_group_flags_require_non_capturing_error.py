from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_flags_require_non_capturing_error() -> NoReturn:
    """Raise a structured ValidationError when scoped flags are combined with capturing=True."""
    raise ValidationError(
        error_name="GROUP_FLAGS_REQUIRE_NON_CAPTURING",
        label="Group modifiers",
        value="flags, capturing=True",
        problem=(
            "`flags`/`flags_off` require `capturing=False` — Python's `re` scoped-flag syntax `(?flags:...)` is always non-capturing.",
            "Scoped flag groups in Python regex cannot capture text.",
        ),
        expected="capturing=False when scoped flags are specified.",
        how_to_fix=(
            "Set `capturing=False` when using `flags` or `flags_off`.",
        ),
        exception=ValueError,
    )