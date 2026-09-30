from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_variable_length_lookbehind_error(inner: Any) -> NoReturn:
    """Raise a structured ValidationError when a lookbehind's inner node has no fixed length."""
    raise ValidationError(
        error_name="VARIABLE_LENGTH_LOOKBEHIND",
        label="Lookbehind inner node",
        value=repr(inner),
        problem=(
            f"Lookaround(direction=BEHIND) requires `inner` to have a fixed length, but {inner!r}.fixed_length() returned None.",
            "Python's `re` engine cannot compile a variable-length lookbehind assertion.",
        ),
        expected="An inner regex node that yields a constant fixed length.",
        how_to_fix=(
            "Ensure that every branch of an inner Alternation or Repeat has a guaranteed fixed length.",
            "Check that no component inside the lookbehind varies in length or uses unbound quantifiers.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_variable_length_lookbehind_error — Variable-Length Lookbehind Validation

## Purpose
Enforces Point 3 at construction time by catching variable-length nodes inside 
backward lookarounds (`LookaroundDirection.BEHIND`) before handing them to Python's `re.compile()`.
"""