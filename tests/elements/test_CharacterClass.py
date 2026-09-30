from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.elements.CharacterRange import CharacterRange

def test_character_class_patterns():
    """Verify CharacterClass pattern generation and fixed length."""
    cc = CharacterClass(Literal("a"), Literal("b"), Literal("c"))
    assert cc.to_pattern() == "[abc]"
    assert cc.fixed_length() == 1

    cc_neg = CharacterClass(CharacterRange("a", "z"), negate=True)
    assert cc_neg.to_pattern() == "[^a-z]"