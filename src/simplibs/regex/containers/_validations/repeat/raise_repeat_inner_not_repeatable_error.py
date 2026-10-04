from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_repeat_inner_not_repeatable_error(
    inner: Any
) -> NoReturn:
    """Raise a ParamError when Repeat receives a node a quantifier cannot follow
    directly (a bare Anchor).

    Args:
        inner: The node that cannot be repeated.

    Raises:
        ParamError: Always.
    """
    node_type = type(inner).__name__

    raise ParamError(
        error_name="REPEAT_INNER_NOT_REPEATABLE_ERROR",
        label="inner",
        expected="a node a quantifier can follow (not a bare Anchor)",
        value=inner,
        problem=(
            f"Repeat() received {node_type} {inner!r}, which cannot be quantified directly.",
            "Python's re rejects a quantifier placed straight after an anchor (for example '^*' or '\\b?') with 'nothing to repeat'.",
        ),
        how_to_fix=(
            "An anchor is zero-width, so repeating it adds nothing — remove the Repeat.",
            f"If you really need it, wrap the node first: Repeat(Group({node_type}(...), capturing=False), ...)",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_repeat_inner_not_repeatable_error — Repeat Inner Guard

## Purpose
Guards Repeat against nodes flagged `_repeatable = False` (currently Anchor), failing at
construction instead of with re's less specific "nothing to repeat" at compile time.
"""
