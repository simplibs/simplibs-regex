import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import (
    raise_character_range_invalid_boundary_error,
)


@pytest.mark.parametrize(
    "name, invalid_val",
    [
        ("start", "abc"),
        ("end", ""),
    ],
)
def test_raise_character_range_invalid_boundary_error_contract(
    subtests,
    name,
    invalid_val,
) -> None:
    """Verify that raise_character_range_invalid_boundary_error raises ValidationError wrapping ValueError."""
    received_type = type(invalid_val).__name__

    assert_exception_function(
        subtests,
        raise_character_range_invalid_boundary_error,
        invalid_params=(name, invalid_val),
        exception_type=ValidationError,
        error_name="CHARACTER_RANGE_INVALID_BOUNDARY",
        label=name,
        value=invalid_val,
        problem=(
            f"Character range boundary '{name}' must be a single-character string, but received value {invalid_val!r} of type '{received_type}'.",
            "Character ranges (`a-z`) can only span between individual single characters.",
        ),
        expected="A single-character string (e.g., 'a', 'Z', '0').",
        how_to_fix=(
            f"Provide a single character for the `{name}` boundary.",
            "Example: CharacterRange('a', 'z')",
        ),
        exception=ValueError,
        verbose=False,
    )