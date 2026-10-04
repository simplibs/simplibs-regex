import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_repeat_inner_not_repeatable_error,
)
from simplibs.regex.elements.Anchor import Anchor, AnchorKind


@pytest.mark.parametrize(
    "inner",
    [
        Anchor(AnchorKind.START),
        Anchor(AnchorKind.WORD_BOUNDARY),
        Anchor(AnchorKind.END_STRING),
    ],
)
def test_raise_repeat_inner_not_repeatable_error_contract(
    subtests,
    inner,
) -> None:
    """Verify that raise_repeat_inner_not_repeatable_error raises ParamError
    wrapping ValueError when Repeat receives a node a quantifier cannot follow."""

    node_type = type(inner).__name__

    assert_exception_function(
        subtests,
        raise_repeat_inner_not_repeatable_error,
        invalid_params=(inner,),
        exception_type=ParamError,
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
        verbose=False,
    )
