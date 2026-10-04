import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.compiler._validations import (
    raise_param_invalid_type_error,
)


@pytest.mark.parametrize(
    "param_name, expected, value, example",
    [
        ("node", "a Regex instance", "abc", None),
        ("flags", "a set or frozenset of Flag members", ["i"], "frozenset({Flag.IGNORECASE})"),
        ("description", "a str", 5, None),
        ("lazy", "a bool", "yes", None),
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
    wrapping TypeError when a parameter has the wrong type[cite: 24]."""

    received_type = type(value).__name__
    how_to_fix = (f"Pass {expected} for parameter '{param_name}'.",)
    if example:
        how_to_fix += (f"Example: {example}",)

    assert_exception_function(
        subtests,
        raise_param_invalid_type_error,
        invalid_params=(param_name, value),  # Zde předáváme už jen 2 argumenty, které funkce akceptuje
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