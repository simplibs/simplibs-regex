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