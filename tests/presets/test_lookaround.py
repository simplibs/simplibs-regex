from typing import Any

import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.lookaround import (
    LOOKAHEAD,
    NEGATIVE_LOOKAHEAD,
    LOOKBEHIND,
    NEGATIVE_LOOKBEHIND,
)
from simplibs.regex.presets.quantifiers import ONE_OR_MORE, ZERO_OR_MORE
from simplibs.regex.testing import assert_pattern


# Lookarounds are zero-width, so each one is tested inside a small sequence
# that consumes real text around it.
@pytest.mark.parametrize(
    ("preset", "expected"),
    [
        (LOOKAHEAD, "(?=abc)"),
        (NEGATIVE_LOOKAHEAD, "(?!abc)"),
        (LOOKBEHIND, "(?<=abc)"),
        (NEGATIVE_LOOKBEHIND, "(?<!abc)"),
    ],
    ids=["LOOKAHEAD", "NEGATIVE_LOOKAHEAD", "LOOKBEHIND", "NEGATIVE_LOOKBEHIND"],
)
def test_lookaround_pattern(subtests: Any, preset: Any, expected: str) -> None:
    """Test the pattern string of every lookaround preset."""
    assert_pattern(subtests, preset(Literal("abc")), expected)


def test_lookahead(subtests: Any) -> None:
    """Test that the next text must match, without consuming it."""
    node = Literal("a") + LOOKAHEAD(Literal("b")) + Literal("b")
    assert_pattern(subtests, node, "a(?=b)b", matches=["ab"], non_matches=["ac", "a"])


def test_negative_lookahead(subtests: Any) -> None:
    """Test that the next text must NOT match."""
    node = Literal("a") + NEGATIVE_LOOKAHEAD(Literal("b")) + Literal("c")
    assert_pattern(subtests, node, "a(?!b)c", matches=["ac"], non_matches=["abc", "a"])


def test_lookbehind(subtests: Any) -> None:
    """Test that the preceding text must match."""
    node = Literal("a") + LOOKBEHIND(Literal("a")) + Literal("b")
    assert_pattern(subtests, node, "a(?<=a)b", matches=["ab"], non_matches=["b", "ac"])


def test_negative_lookbehind(subtests: Any) -> None:
    """Test that the preceding text must NOT match."""
    node = (Literal("a") | Literal("b")) + NEGATIVE_LOOKBEHIND(Literal("b")) + Literal("c")
    assert_pattern(
        subtests, node, "(?:a|b)(?<!b)c",
        matches=["ac"], non_matches=["bc", "c"],
    )


def test_lookbehind_accepts_equal_length_alternatives(subtests: Any) -> None:
    """Test that same-width branches are a legal lookbehind."""
    node = Literal("cat") + LOOKBEHIND(Literal("cat") | Literal("dog")) + Literal("s")
    assert_pattern(
        subtests, node, "cat(?<=cat|dog)s",
        matches=["cats"], non_matches=["cat", "dogs"],
    )


@pytest.mark.parametrize("factory", [LOOKBEHIND, NEGATIVE_LOOKBEHIND])
def test_lookbehind_rejects_variable_length(factory: Any) -> None:
    """Test that a variable-length lookbehind fails at construction."""
    with pytest.raises(ValueError):
        factory(ZERO_OR_MORE(DIGIT))


def test_lookbehind_example_from_the_readme() -> None:
    """`LOOKBEHIND(Literal("USD")) + ONE_OR_MORE(DIGIT)` finds digits only after "USD"."""
    node = LOOKBEHIND(Literal("USD")) + ONE_OR_MORE(DIGIT)
    assert node.to_pattern() == "(?<=USD)\\d+"
    assert RegexPattern(node).search("USD42").group() == "42"
    assert RegexPattern(node).search("EUR42") is None
