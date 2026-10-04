import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_param_invalid_type_error,
)


@pytest.mark.parametrize(
    "param_name, expected, value, example",
    [
        ("inner", "a Regex instance", "abc", None),
        ("negate", "a bool", 1, None),
        ("min", "an int (booleans are not accepted)", True, "Repeat(DIGIT, min=1)"),
        ("flags", "a set or frozenset of Flag members, or None", ["i"], "frozenset({Flag.IGNORECASE})"),
        ("name", "a str or None", 5, None),
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
        invalid_params=(param_name, value),
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