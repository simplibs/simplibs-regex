import pytest
from simplibs.regex.elements.RawPattern import RawPattern
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.containers.Sequence import Sequence


def test_raw_pattern_basic() -> None:
    """Test basic initialization and verbatim pattern production."""
    node = RawPattern(r"a{2,4}")
    assert node.to_pattern() == r"a{2,4}"


def test_raw_pattern_invalid_type() -> None:
    """Test that passing a non-string raises TypeError."""
    with pytest.raises(TypeError, match="requires a str"):
        RawPattern(123)  # type: ignore[arg-type]


def test_raw_pattern_empty_string() -> None:
    """Test that passing an empty string raises ValueError."""
    with pytest.raises(ValueError, match="requires a non-empty string"):
        RawPattern("")


def test_raw_pattern_fixed_length() -> None:
    """Test that fixed_length always returns None for raw text."""
    node = RawPattern(r"abc")
    assert node.fixed_length() is None


def test_raw_pattern_precedence_wrapping() -> None:
    """Test that RawPattern wraps correctly in non-capturing group inside Sequence

    (since its precedence is ALTERNATION, which is lower than SEQUENCE).
    """
    node = Sequence(RawPattern(r"a|b"), RawPattern(r"c"))
    # Sequence precedence is SEQUENCE (1), RawPattern precedence is ALTERNATION (0).
    # ALTERNATION < SEQUENCE -> must wrap both in (?:...)
    assert node.to_pattern() == "(?:a|b)(?:c)"


def test_raw_pattern_compilation_and_search() -> None:
    """Test integration with RegexPattern for actual text searching."""
    pattern = RegexPattern(RawPattern(r"\b\d{3}\b"))

    match = pattern.search("Item 123 found")
    assert match is not None
    assert match.group(0) == "123"

    assert pattern.search("No digits here") is None