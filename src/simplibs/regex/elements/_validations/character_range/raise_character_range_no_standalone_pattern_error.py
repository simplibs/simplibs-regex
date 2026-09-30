from typing import NoReturn
from simplibs.exception import ParamError


def raise_character_range_no_standalone_pattern_error() -> NoReturn:
    """Raise a structured ParamError when CharacterRange.to_pattern() is called standalone."""
    raise ParamError(
        error_name="CHARACTER_RANGE_NO_STANDALONE_PATTERN",
        label="CharacterRange pattern",
        value="standalone",
        problem=(
            "CharacterRange has no standalone pattern — it is only valid as an item inside CharacterClass(...).",
            "A character range cannot be rendered outside a character class context.",
        ),
        expected="Embedding inside a CharacterClass.",
        how_to_fix=(
            "Wrap the CharacterRange inside CharacterClass(CharacterRange(...)).",
        ),
        exception=TypeError,
    )