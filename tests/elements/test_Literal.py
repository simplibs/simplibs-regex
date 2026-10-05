import re
import pytest
from simplibs.exception import ValidationError
from simplibs.regex.containers.Repeat import Repeat
from simplibs.regex.elements.Literal import Literal

TRICKY_TEXTS = ["a.b", "3+3=6", "(x)", "[a]", "$^", "a b", "a #b", "\n", "\\", "ěščř", "tab\t"]


def test_literal_pattern_is_escaped():
    """Regex-special characters are escaped; plain text is untouched."""
    assert Literal("abc").to_pattern() == "abc"
    assert Literal("a.b").to_pattern() == "a\\.b"
    assert Literal("3+3=6").to_pattern() == "3\\+3=6"


@pytest.mark.parametrize(
    ("char", "escape"),
    [("\t", "\\t"), ("\n", "\\n"), ("\r", "\\r"), ("\f", "\\f"), ("\v", "\\v"), ("\a", "\\a"),
     ("\x00", "\\x00"), ("\x08", "\\x08"), ("\x1f", "\\x1f"), ("\x7f", "\\x7f")],
)
def test_literal_writes_control_characters_as_readable_escapes(char, escape):
    """`\\n` instead of a backslash plus an invisible newline; behaviour is identical."""
    assert Literal(char).to_pattern() == escape
    assert re.fullmatch(escape, char) is not None


def test_literal_keeps_a_space_escaped_and_mixes_text_with_controls():
    assert Literal(" ").to_pattern() == "\\ "
    assert Literal("a\tb").to_pattern() == "a\\tb"
    assert Literal("a.\n").to_pattern() == "a\\.\\n"


def test_literal_keeps_the_original_unescaped_text():
    assert Literal("a.b").text == "a.b"
    assert Literal("\n").text == "\n"


@pytest.mark.parametrize("text", TRICKY_TEXTS)
def test_literal_matches_exactly_its_own_text(text):
    """The rendered pattern matches the text it was built from — and nothing longer."""
    compiled = re.compile(Literal(text).to_pattern())
    assert compiled.fullmatch(text) is not None
    assert compiled.fullmatch(text + "x") is None


def test_literal_is_safe_under_the_verbose_flag():
    """Spaces and `#` are escaped, so VERBOSE does not swallow them."""
    compiled = re.compile(Literal("a #b").to_pattern(), re.VERBOSE)
    assert compiled.fullmatch("a #b") is not None


@pytest.mark.parametrize(
    ("text", "length"),
    [("a", 1), ("abc", 3), ("a.b", 3), ("ěščř", 4)],
)
def test_literal_fixed_length_is_the_unescaped_length(text, length):
    assert Literal(text).fixed_length() == length


@pytest.mark.parametrize(("text", "needs_wrap"), [("a", False), ("ab", True), ("a.b", True)])
def test_literal_needs_wrap_for_repeat_only_when_longer_than_one_char(text, needs_wrap):
    assert Literal(text).needs_wrap_for_repeat() is needs_wrap


def test_literal_is_wrapped_by_repeat_only_when_needed():
    """Integration: a multi-character Literal must be repeated as a whole."""
    assert Repeat(Literal("ab"), min=3, max=3).to_pattern() == "(?:ab){3}"
    assert Repeat(Literal("a"), min=3, max=3).to_pattern() == "a{3}"


def test_literal_concatenates_with_plus():
    assert (Literal("ab") + Literal("c")).to_pattern() == "abc"


@pytest.mark.parametrize(
    ("char", "fragment"),
    [
        ("a", "a"), (".", "."), ("+", "+"),                     # not special inside [...]
        ("]", "\\]"), ("^", "\\^"), ("-", "\\-"), ("\\", "\\\\"),
        ("\t", "\\t"), ("\n", "\\n"), ("\r", "\\r"), ("\x08", "\\x08"),    # control characters stay readable
        ("[", "\\["), ("&", "\\&"), ("~", "\\~"), ("|", "\\|"),  # reserved by `re` for set operations
    ],
)
def test_literal_char_class_fragment_escapes_only_class_specials(char, fragment):
    assert Literal(char).to_char_class_fragment() == fragment


def test_literal_char_class_fragment_rejects_longer_text():
    with pytest.raises(ValidationError):
        Literal("ab").to_char_class_fragment()


def test_literal_rejects_empty_text():
    with pytest.raises(ValidationError):
        Literal("")


@pytest.mark.parametrize("bad", [5, None, b"abc", ["a"]])
def test_literal_rejects_non_string(bad):
    """Type check comes from @validate_call."""
    with pytest.raises(ValidationError):
        Literal(bad)
from simplibs.regex.elements.Literal import Literal

def test_literal():
    """Verify Literal pattern generation, fixed length, and repeat wrapping."""
    lit = Literal("a.b")
    assert lit.to_pattern() == "a\\.b"
    assert lit.fixed_length() == 3
    assert lit.needs_wrap_for_repeat() is True

    lit_single = Literal("a")
    assert lit_single.needs_wrap_for_repeat() is False
    assert lit_single.to_char_class_fragment() == "a"