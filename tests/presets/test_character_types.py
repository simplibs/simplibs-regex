import pytest
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.CharacterType import CharacterType, CharacterTypeKind
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.character_types import (
    DIGIT, NON_DIGIT, WORD_CHARACTER, NON_WORD_CHARACTER, WHITESPACE, NON_WHITESPACE,
)
from simplibs.regex.testing import assert_pattern


CASES = [
    (DIGIT, '\\d', ['0', '5'], ['a', ' ', '55'], frozenset()),
    (NON_DIGIT, '\\D', ['a', ' ', '-'], ['5'], frozenset()),
    (WORD_CHARACTER, '\\w', ['a', 'Z', '9', '_'], [' ', '-', '!'], frozenset()),
    (NON_WORD_CHARACTER, '\\W', [' ', '-', '!'], ['a', '5', '_'], frozenset()),
    (WHITESPACE, '\\s', [' ', '\t', '\n'], ['a', '5'], frozenset()),
    (NON_WHITESPACE, '\\S', ['a', '5', '!'], [' ', '\t', '\n'], frozenset()),
    (DIGIT, '\\d', ['5'], ['٣'], frozenset({Flag.ASCII})),
    (DIGIT, '\\d', ['5', '٣'], ['a'], frozenset()),
]


@pytest.mark.parametrize(("node", "expected", "matches", "non_matches", "flags"), CASES)
def test_character_types_presets(subtests, node, expected, matches, non_matches, flags) -> None:
    """Each preset renders the documented pattern and matches / rejects the documented texts."""
    assert_pattern(
        subtests, node, expected,
        matches=matches, non_matches=non_matches, flags=flags,
    )


@pytest.mark.parametrize(
    ("preset", "kind"),
    [
        (DIGIT, CharacterTypeKind.DIGIT), (NON_DIGIT, CharacterTypeKind.NON_DIGIT),
        (WORD_CHARACTER, CharacterTypeKind.WORD_CHARACTER), (NON_WORD_CHARACTER, CharacterTypeKind.NON_WORD_CHARACTER),
        (WHITESPACE, CharacterTypeKind.WHITESPACE), (NON_WHITESPACE, CharacterTypeKind.NON_WHITESPACE),
    ],
    ids=["DIGIT", "NON_DIGIT", "WORD_CHARACTER", "NON_WORD_CHARACTER", "WHITESPACE", "NON_WHITESPACE"],
)
def test_character_type_preset_is_the_right_kind(preset, kind) -> None:
    """Each preset is a CharacterType of the matching kind."""
    assert isinstance(preset, CharacterType)
    assert preset.kind is kind


def test_character_types_are_legal_class_items(subtests) -> None:
    """Unlike `.`, these escapes keep their meaning inside `[...]`."""
    assert_pattern(
        subtests, CharacterClass(DIGIT, WHITESPACE), "[\\d\\s]",
        matches=["5", " "], non_matches=["a"],
    )
