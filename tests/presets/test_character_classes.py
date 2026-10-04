import pytest
from simplibs.regex.presets.character_classes import (
    LOWERCASE_LETTER, UPPERCASE_LETTER, LETTER, ALPHANUMERIC, HEX_DIGIT,
)
from simplibs.regex.presets.quantifiers import ONE_OR_MORE
from simplibs.regex.testing import assert_pattern


CASES = [
    (LOWERCASE_LETTER, '[a-z]', ['a', 'z'], ['A', '5', 'é', 'ab']),
    (UPPERCASE_LETTER, '[A-Z]', ['A', 'Z'], ['a', '5', 'É']),
    (LETTER, '[a-zA-Z]', ['a', 'Z'], ['5', '_', 'é']),
    (ALPHANUMERIC, '[a-zA-Z0-9]', ['a', 'Z', '5'], ['_', '-', 'é', '٣']),
    (HEX_DIGIT, '[0-9a-fA-F]', ['0', '9', 'a', 'F'], ['g', 'G', '-', '٣']),
]


@pytest.mark.parametrize(("node", "expected", "matches", "non_matches"), CASES)
def test_character_classes_presets(subtests, node, expected, matches, non_matches) -> None:
    """Each preset renders the documented pattern and matches / rejects the documented texts."""
    assert_pattern(subtests, node, expected, matches=matches, non_matches=non_matches)


def test_character_classes_compose_with_quantifiers(subtests):
    assert_pattern(
        subtests, ONE_OR_MORE(HEX_DIGIT), "[0-9a-fA-F]+",
        matches=["ff00", "A1"], non_matches=["", "xyz"],
    )
