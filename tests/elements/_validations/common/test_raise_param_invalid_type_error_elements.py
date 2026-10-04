import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_param_invalid_type_error,
)


@pytest.mark.parametrize(
    "param_name, expected, value, example",
    [
        ("text", "a str", 5, 'Literal("abc")'),
        ("text", "a str", None, None),
        ("kind", "an AnchorKind member", "START", "AnchorKind.START_STRING"),
        ("kind", "a CharacterTypeKind member", 3.14, None),
    ],
)
def test_raise_param_invalid_type_error_contract(
    subtests,
    param_name,
    expected,
    value,
    example,
) -> None:
    """Verify that raise_param_invalid_type_error raises ParamError
    wrapping TypeError when a parameter has the wrong type."""

    received_type = type(value).__name__
    how_to_fix = (f"Pass {expected} for parameter '{param_name}'.",)
    if example:
        how_to_fix += (f"Example: {example}",)

    assert_exception_function(
        subtests,
        raise_param_invalid_type_error,
        invalid_params=(param_name, expected, value, example),
        exception_type=ParamError,
        error_name="PARAM_INVALID_TYPE_ERROR",
        label=param_name,
        expected=expected,
        value=value,
        problem=(
            f"Parameter '{param_name}' received {value!r} of type '{received_type}'.",
            f"Expected {expected}.",
        ),
        how_to_fix=how_to_fix,
        exception=TypeError,
        verbose=False,
    )
