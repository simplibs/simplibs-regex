from typing import Any

import pytest
from simplibs.exception import ValidationError
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.CharacterRange import CharacterRange
from simplibs.regex.testing import assert_pattern


@pytest.mark.parametrize(
    ("start", "end", "fragment"),
    [
        ("a", "z", "a-z"),
        ("0", "9", "0-9"),
        ("a", "a", "a-a"),
        ("]", "a", "\\]-a"),
        ("^", "a", "\\^-a"),
        ("\\", "^", "\\\\-\\^"),
    ],
)
def test_character_range_fragment(start: str, end: str, fragment: str) -> None:
    """Test the class fragment, including escaped boundary characters."""
    assert CharacterRange(start, end).to_char_class_fragment() == fragment


def test_character_range_fixed_length() -> None:
    """Test that a range counts as one character."""
    assert CharacterRange("a", "z").fixed_length() == 1


def test_character_range_standalone_pattern_raises() -> None:
    """Test that a range has no meaning outside a CharacterClass."""
    with pytest.raises(ValidationError):
        CharacterRange("a", "z").to_pattern()


def test_character_range_usable_in_char_class() -> None:
    """Test that a range opts into CharacterClass usage."""
    assert CharacterRange._usable_in_char_class is True


@pytest.mark.parametrize(
    ("start", "end", "expected", "matches", "non_matches"),
    [
        ("a", "z", "[a-z]", ["a", "m", "z"], ["A", "0", "az", ""]),
        ("]", "a", "[\\]-a]", ["]", "^", "_", "`", "a"], ["A", "b"]),
        ("\\", "^", "[\\\\-\\^]", ["\\", "]", "^"], ["a"]),
    ],
)
def test_character_range_inside_class(
    subtests: Any,
    start: str,
    end: str,
    expected: str,
    matches: list[str],
    non_matches: list[str],
) -> None:
    """Test a range end to end inside a CharacterClass."""
    assert_pattern(
        subtests, CharacterClass(CharacterRange(start, end)), expected,
        matches=matches, non_matches=non_matches,
    )


@pytest.mark.parametrize(
    ("start", "end"),
    [("ab", "z"), ("a", "yz"), ("", "z"), ("a", ""), (1, "z"), ("a", None)],
)
def test_character_range_invalid_boundary(start: object, end: object) -> None:
    """Test that both boundaries must be single characters."""
    with pytest.raises((TypeError, ValueError)):
        CharacterRange(start, end)  # type: ignore[arg-type]


def test_character_range_start_after_end() -> None:
    """Test that a reversed range is rejected at construction."""
    with pytest.raises(ValueError):
        CharacterRange("z", "a")