from typing import Any

import pytest
from simplibs.regex.elements.AnyCharacter import AnyCharacter
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.any_character import ANY
from simplibs.regex.testing import assert_pattern


def test_any_is_an_any_character() -> None:
    """Test that the preset is an AnyCharacter instance."""
    assert isinstance(ANY, AnyCharacter)


def test_any_pattern_and_matching(subtests: Any) -> None:
    """Test that ANY renders `.` and matches one non-newline character."""
    assert_pattern(
        subtests, ANY, ".",
        matches=["a", "5", " ", "!", "\t"],
        non_matches=["\n", "", "ab"],
    )


def test_any_with_dotall_matches_newline(subtests: Any) -> None:
    """Test that the DOTALL flag makes ANY match a newline too."""
    assert_pattern(
        subtests, ANY, ".",
        matches=["a", "\n"], non_matches=["ab"],
        flags=frozenset({Flag.DOTALL}),
    )


def test_any_is_not_usable_in_a_class() -> None:
    """Test that `[.]` (a literal dot) cannot be built by accident."""
    with pytest.raises(TypeError):
        CharacterClass(ANY)

