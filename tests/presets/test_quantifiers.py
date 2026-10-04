from typing import Any

import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.containers.enums import RepeatMode
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.groups import NON_CAPTURING
from simplibs.regex.presets.quantifiers import (
    OPTIONAL,
    ZERO_OR_MORE,
    ONE_OR_MORE,
    EXACTLY,
    AT_LEAST,
    BETWEEN,
)
from simplibs.regex.testing import assert_pattern

A = Literal("a")


def test_optional(subtests: Any) -> None:
    """Test `?`."""
    assert_pattern(subtests, OPTIONAL(A), "a?", matches=["", "a"], non_matches=["aa", "b"])


def test_zero_or_more(subtests: Any) -> None:
    """Test `*`."""
    assert_pattern(
        subtests, ZERO_OR_MORE(A), "a*",
        matches=["", "a", "aaa"], non_matches=["b", "ab"],
    )


def test_one_or_more(subtests: Any) -> None:
    """Test `+`."""
    assert_pattern(
        subtests, ONE_OR_MORE(A), "a+",
        matches=["a", "aaa"], non_matches=["", "b"],
    )


def test_exactly(subtests: Any) -> None:
    """Test `{n}`."""
    assert_pattern(
        subtests, EXACTLY(A, 3), "a{3}",
        matches=["aaa"], non_matches=["aa", "aaaa"],
    )


def test_at_least(subtests: Any) -> None:
    """Test `{n,}`."""
    assert_pattern(
        subtests, AT_LEAST(A, 2), "a{2,}",
        matches=["aa", "aaaaa"], non_matches=["", "a"],
    )


def test_between(subtests: Any) -> None:
    """Test `{m,n}`."""
    assert_pattern(
        subtests, BETWEEN(A, 2, 4), "a{2,4}",
        matches=["aa", "aaa", "aaaa"], non_matches=["a", "aaaaa"],
    )


def test_multi_character_literal_is_wrapped(subtests: Any) -> None:
    """Test that a quantifier applies to the whole literal, not its last letter."""
    ab = Literal("ab")
    assert_pattern(
        subtests, EXACTLY(ab, 3), "(?:ab){3}",
        matches=["ababab"], non_matches=["ab", "abbb"],
    )
    assert_pattern(
        subtests, OPTIONAL(ab), "(?:ab)?",
        matches=["", "ab"], non_matches=["a"],
    )


@pytest.mark.parametrize(
    ("node", "expected"),
    [
        (ZERO_OR_MORE(A, mode=RepeatMode.LAZY), "a*?"),
        (ONE_OR_MORE(A, mode=RepeatMode.LAZY), "a+?"),
        (AT_LEAST(A, 2, mode=RepeatMode.LAZY), "a{2,}?"),
        (BETWEEN(A, 2, 4, mode=RepeatMode.LAZY), "a{2,4}?"),
        (ZERO_OR_MORE(A, mode=RepeatMode.POSSESSIVE), "a*+"),
        (ONE_OR_MORE(A, mode=RepeatMode.POSSESSIVE), "a++"),
        (AT_LEAST(A, 2, mode=RepeatMode.POSSESSIVE), "a{2,}+"),
        (BETWEEN(A, 2, 4, mode=RepeatMode.POSSESSIVE), "a{2,4}+"),
    ],
)
def test_modes_pattern(subtests: Any, node: Any, expected: str) -> None:
    """Test the pattern string of every non-greedy mode."""
    assert_pattern(subtests, node, expected)


def test_lazy_takes_the_shortest_match() -> None:
    """Test that LAZY and GREEDY differ in how much text they take."""
    text = "aaa"
    greedy = RegexPattern(ONE_OR_MORE(A)).search(text)
    lazy = RegexPattern(ONE_OR_MORE(A, mode=RepeatMode.LAZY)).search(text)
    assert greedy is not None and greedy.group() == "aaa"
    assert lazy is not None and lazy.group() == "a"


def test_possessive_never_gives_back() -> None:
    """Test that a possessive quantifier blocks backtracking."""
    greedy = RegexPattern(ONE_OR_MORE(A) + A)
    possessive = RegexPattern(ONE_OR_MORE(A, mode=RepeatMode.POSSESSIVE) + A)
    assert greedy.search("aaa") is not None
    assert possessive.search("aaa") is None


def test_single_token_nodes_are_not_wrapped(subtests: Any) -> None:
    """A character type or a group is already one token: no extra `(?:...)`."""
    assert_pattern(subtests, EXACTLY(DIGIT, 3), "\\d{3}", matches=["123"], non_matches=["12"])
    assert_pattern(
        subtests, ZERO_OR_MORE(NON_CAPTURING(Literal("ab"))), "(?:ab)*",
        matches=["", "abab"], non_matches=["aba"],
    )


def test_nested_quantifier_is_wrapped(subtests: Any) -> None:
    """A quantified node under another quantifier is wrapped: `(?:a+)*`, never `a+*`."""
    assert_pattern(
        subtests, ZERO_OR_MORE(ONE_OR_MORE(A)), "(?:a+)*",
        matches=["", "a", "aaa"], non_matches=["b"],
    )
