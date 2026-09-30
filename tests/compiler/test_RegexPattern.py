import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag

def test_regex_pattern_execution():
    """Verify RegexPattern compilation and core operations (search, match, findall, sub, etc.)."""
    pattern = RegexPattern(Literal("test"))

    # Test pattern string property
    assert pattern.pattern_string == "test"

    # Test search
    assert pattern.search("this is a test string") is not None
    assert pattern.search("no match here") is None

    # Test match
    assert pattern.match("test string") is not None
    assert pattern.match("string test") is None

    # Test fullmatch
    assert pattern.fullmatch("test") is not None
    assert pattern.fullmatch("test string") is None

    # Test findall
    multi_pattern = RegexPattern(Literal("a"))
    assert multi_pattern.findall("banana") == ["a", "a", "a"]

    # Test sub
    assert pattern.sub("passed", "this is a test") == "this is a passed"

    # Test split
    split_pattern = RegexPattern(Literal("-"))
    assert split_pattern.split("a-b-c") == ["a", "b", "c"]

def test_regex_pattern_with_flags():
    """Verify RegexPattern compilation with top-level flags."""
    pattern = RegexPattern(Literal("TEST"), flags=frozenset({Flag.IGNORECASE}))
    assert pattern.search("hello test world") is not None