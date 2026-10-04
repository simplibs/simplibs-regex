from typing import NoReturn
from simplibs.exception import ValidationError


def raise_character_range_no_standalone_pattern_error() -> NoReturn:
    """Raise a structured ValidationError when CharacterRange.to_pattern() is called."""
    raise ValidationError(
        error_name="CHARACTER_RANGE_NO_STANDALONE_PATTERN",
        label="CharacterRange",
        value="CharacterRange",
        problem=(
            "CharacterRange cannot be compiled as a standalone pattern.",
            "A character range (like 'a-z') only has meaning inside a CharacterClass `[...]`.",
        ),
        expected="CharacterRange nested within a CharacterClass.",
        how_to_fix=(
            "Wrap the CharacterRange inside a CharacterClass.",
            "Example: CharacterClass(CharacterRange('a', 'z'))",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_range_no_standalone_pattern_error — Standalone CharacterRange Guard

## Purpose
Guards against attempting to render a CharacterRange as a standalone regex pattern,
ensuring it is properly wrapped inside a CharacterClass.
"""