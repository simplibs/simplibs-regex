from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_atomic_and_name_conflict_error() -> NoReturn:
    """Raise a structured ValidationError when atomic=True is combined with a group name."""
    raise ValidationError(
        error_name="GROUP_ATOMIC_AND_NAME_CONFLICT",
        label="Group modifiers",
        value="atomic=True, name",
        problem=(
            "`atomic=True` cannot be combined with `name`.",
            "Python's `re` syntax does not support atomic named groups in a single construct.",
        ),
        expected="Only one structural modifier (atomic or name) per group.",
        how_to_fix=(
            "Use either an atomic group or a named group, but not both simultaneously.",
        ),
        exception=ValueError,
    )