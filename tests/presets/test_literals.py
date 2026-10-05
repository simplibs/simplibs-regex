import pytest
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.literals import (
    TAB, NEWLINE, CARRIAGE_RETURN, FORM_FEED, VERTICAL_TAB, BELL, BACKSLASH_CHAR,
)
from simplibs.regex.testing import assert_pattern


CASES = [
    (TAB, '\\t', ['\t'], ['t', '\\t', ' ']),
    (NEWLINE, '\\n', ['\n'], ['n', '\r']),
    (CARRIAGE_RETURN, '\\r', ['\r'], ['\n']),
    (FORM_FEED, '\\f', ['\x0c'], [' ']),
    (VERTICAL_TAB, '\\v', ['\x0b'], ['v']),
    (BELL, '\\a', ['\x07'], ['a']),
    (BACKSLASH_CHAR, '\\\\', ['\\'], ['/', '\\\\']),
]


@pytest.mark.parametrize(("node", "expected", "matches", "non_matches"), CASES)
def test_literals_presets(subtests, node, expected, matches, non_matches) -> None:
    """Each preset renders the documented pattern and matches / rejects the documented texts."""
    assert_pattern(subtests, node, expected, matches=matches, non_matches=non_matches)


def test_literals_concatenate_with_other_literals(subtests):
    assert_pattern(
        subtests, Literal("a") + TAB + Literal("b"), "a\\tb",
        matches=["a\tb"], non_matches=["ab", "a b"],
    )


def test_literals_are_legal_character_class_items(subtests):
    """Single-character Literals may appear inside `[...]`; a backslash is escaped there."""
    assert_pattern(
        subtests, CharacterClass(TAB, NEWLINE), "[\\t\\n]",
        matches=["\t", "\n"], non_matches=["a", " "],
    )
    assert_pattern(
        subtests, CharacterClass(BACKSLASH_CHAR), "[\\\\]",
        matches=["\\"], non_matches=["/"],
    )
