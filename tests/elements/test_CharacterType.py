from typing import Any

import pytest
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.CharacterType import CharacterType, CharacterTypeKind
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.testing import assert_pattern

_CASES = [
    (CharacterTypeKind.DIGIT, "\\d", ["0", "5"], ["a", " ", "55", ""]),
    (CharacterTypeKind.NON_DIGIT, "\\D", ["a", " ", "-"], ["5", "ab"]),
    (CharacterTypeKind.WORD_CHARACTER, "\\w", ["a", "Z", "9", "_"], [" ", "-", "!"]),
    (CharacterTypeKind.NON_WORD_CHARACTER, "\\W", [" ", "-", "!"], ["a", "_", "9"]),
    (CharacterTypeKind.WHITESPACE, "\\s", [" ", "\t", "\n"], ["a", "5"]),
    (CharacterTypeKind.NON_WHITESPACE, "\\S", ["a", "5", "-"], [" ", "\n"]),
]


@pytest.mark.parametrize(
    ("kind", "expected", "matches", "non_matches"),
    _CASES,
    ids=[case[0].name for case in _CASES],
)
def test_character_type_pattern_and_matching(
    subtests: Any,
    kind: CharacterTypeKind,
    expected: str,
    matches: list[str],
    non_matches: list[str],
) -> None:
    """Test the pattern string and matching behaviour of every kind."""
    assert_pattern(
        subtests, CharacterType(kind), expected,
        matches=matches, non_matches=non_matches,
    )


@pytest.mark.parametrize("kind", list(CharacterTypeKind))
def test_character_type_fixed_length(kind: CharacterTypeKind) -> None:
    """Test that every kind matches exactly one character."""
    assert CharacterType(kind).fixed_length() == 1


def test_character_type_stores_kind() -> None:
    """Test that the kind is kept on the instance."""
    assert CharacterType(CharacterTypeKind.WORD_CHARACTER).kind is CharacterTypeKind.WORD_CHARACTER


def test_character_type_invalid_kind() -> None:
    """Test that anything other than a CharacterTypeKind is rejected."""
    with pytest.raises(TypeError):
        CharacterType("d")  # type: ignore[arg-type]


def test_character_type_usable_in_char_class(subtests: Any) -> None:
    """Test that the six classes keep their meaning inside `[...]`."""
    assert CharacterType._usable_in_char_class is True
    node = CharacterClass(
        CharacterType(CharacterTypeKind.DIGIT),
        CharacterType(CharacterTypeKind.WHITESPACE),
    )
    assert_pattern(subtests, node, "[\\d\\s]", matches=["5", " "], non_matches=["a"])


def test_character_type_digit_is_unicode_unless_ascii(subtests: Any) -> None:
    """Test that `\\d` matches non-ASCII digits unless the ASCII flag is set."""
    digit = CharacterType(CharacterTypeKind.DIGIT)
    arabic_indic_three = "\u0663"

    assert_pattern(
        subtests, digit, "\\d",
        matches=["5", arabic_indic_three], intro="unicode",
    )
    assert_pattern(
        subtests, digit, "\\d",
        matches=["5"], non_matches=[arabic_indic_three],
        flags=frozenset({Flag.ASCII}), intro="ascii",
    )


def test_character_type_has_no_wildcard_member() -> None:
    """Test that `.` stays out of the enum (it lives in AnyCharacter)."""
    assert "ANY" not in CharacterTypeKind.__members__