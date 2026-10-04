from contextlib import contextmanager
from typing import Iterator

import pytest
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.testing.assert_pattern import assert_pattern


class _RecordingSubtests:
    """Minimal stand-in for the pytest-subtests fixture.

    Like the real one, it swallows an AssertionError raised inside a
    subtest and only records it, so the surrounding test keeps running.
    """

    def __init__(self) -> None:
        self.names: list[str] = []
        self.failed: list[str] = []

    @contextmanager
    def test(self, name: str) -> Iterator[None]:
        self.names.append(name)
        try:
            yield
        except AssertionError:
            self.failed.append(name)


def test_valid_pattern_passes_silently() -> None:
    """Test that a correct pattern passes and uses no subtests when not verbose."""
    subtests = _RecordingSubtests()
    assert_pattern(subtests, DIGIT, "\\d", matches=["5"], non_matches=["a", "55"], verbose=False)
    assert subtests.names == []


def test_verbose_registers_one_subtest_per_check() -> None:
    """Test subtest naming and count in verbose mode."""
    subtests = _RecordingSubtests()
    assert_pattern(subtests, DIGIT, "\\d", matches=["5"], non_matches=["a"])
    assert subtests.names == [
        "[\\d] Pattern String Check",
        "[\\d] Match Check ('5')",
        "[\\d] Non-Match Check ('a')",
    ]
    assert subtests.failed == []


def test_intro_replaces_default_prefix() -> None:
    """Test that `intro` replaces the default [pattern] prefix."""
    subtests = _RecordingSubtests()
    assert_pattern(subtests, DIGIT, "\\d", matches=["5"], intro="digit")
    assert subtests.names == ["digit Pattern String Check", "digit Match Check ('5')"]


def test_no_matches_means_only_string_check() -> None:
    """Test that omitted matches/non_matches produce only the string check."""
    subtests = _RecordingSubtests()
    assert_pattern(subtests, DIGIT, "\\d")
    assert subtests.names == ["[\\d] Pattern String Check"]


def test_wrong_pattern_string_raises_when_not_verbose() -> None:
    """Test that a wrong pattern string raises immediately when not verbose."""
    with pytest.raises(AssertionError, match="Expected pattern string"):
        assert_pattern(None, DIGIT, "\\w", verbose=False)


def test_failed_match_raises_when_not_verbose() -> None:
    """Test that a failed positive match raises immediately when not verbose."""
    with pytest.raises(AssertionError, match="' to match value 'a'"):
        assert_pattern(None, DIGIT, "\\d", matches=["a"], verbose=False)


def test_failed_non_match_raises_when_not_verbose() -> None:
    """Test that a failed negative match raises immediately when not verbose."""
    with pytest.raises(AssertionError, match="NOT to match value '5'"):
        assert_pattern(None, DIGIT, "\\d", non_matches=["5"], verbose=False)


def test_verbose_records_failures_and_keeps_going() -> None:
    """Test that verbose mode records every failure and still runs later checks."""
    subtests = _RecordingSubtests()
    assert_pattern(subtests, DIGIT, "\\w", matches=["a", "5"], non_matches=["7"])
    assert subtests.failed == [
        "[\\w] Pattern String Check",
        "[\\w] Match Check ('a')",
        "[\\w] Non-Match Check ('7')",
    ]
    assert "[\\w] Match Check ('5')" in subtests.names


def test_flags_are_applied_to_matching() -> None:
    """Test that `flags` reach the compiled pattern."""
    node = Literal("a")
    assert_pattern(None, node, "a", matches=["A"], flags=frozenset({Flag.IGNORECASE}), verbose=False)
    assert_pattern(None, node, "a", non_matches=["A"], verbose=False)


def test_rejects_non_regex_pattern_obj() -> None:
    """Test that a non-Regex pattern_obj raises TypeError."""
    with pytest.raises(TypeError, match="requires a Regex instance"):
        assert_pattern(None, "\\d", "\\d")  # type: ignore[arg-type]


def test_rejects_bare_string_instead_of_list() -> None:
    """Test that a bare str for matches/non_matches raises TypeError."""
    with pytest.raises(TypeError, match="'matches' must be a list"):
        assert_pattern(None, DIGIT, "\\d", matches="123")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="'non_matches' must be a list"):
        assert_pattern(None, DIGIT, "\\d", non_matches="abc")  # type: ignore[arg-type]