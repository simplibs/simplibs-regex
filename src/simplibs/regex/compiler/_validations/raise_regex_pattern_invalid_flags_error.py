from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_regex_pattern_invalid_flags_error(flags: Any) -> NoReturn:
    """Raise a structured ParamError when RegexPattern() receives invalid flags."""
    raise ParamError(
        error_name="REGEX_PATTERN_INVALID_FLAGS",
        label="RegexPattern flags",
        value=repr(flags),
        problem=(
            f"RegexPattern() requires `flags` to be a frozenset of Flag members, got {flags!r}.",
            "Flags must be provided as a frozen set containing only valid Flag instances.",
        ),
        expected="A frozenset of Flag members.",
        how_to_fix=(
            "Pass flags as a frozenset of Flag objects (e.g. frozenset([Flag.IGNORECASE])).",
        ),
        exception=TypeError,
    )