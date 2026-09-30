from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_name_and_flags_conflict_error() -> NoReturn:
    """Raise a structured ValidationError when a group name is combined with scoped flags."""
    raise ValidationError(
        error_name="GROUP_NAME_AND_FLAGS_CONFLICT",
        label="Group modifiers",
        value="name, flags",
        problem=(
            "`name` cannot be combined with `flags`/`flags_off`.",
            "Python's `re` syntax does not support scoped flags on a named group opening.",
        ),
        expected="Only one structural modifier (name or flags) per group.",
        how_to_fix=(
            "Apply flags in an enclosing group or separate the named group.",
        ),
        exception=ValueError,
    )