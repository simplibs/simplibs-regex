from simplibs.regex.elements.Anchor import Anchor, AnchorKind

def test_anchor_patterns():
    """Verify pattern production and fixed length for Anchor kinds."""
    assert Anchor(AnchorKind.START).to_pattern() == "^"
    assert Anchor(AnchorKind.END).to_pattern() == "$"
    assert Anchor(AnchorKind.START_STRING).to_pattern() == "\\A"
    assert Anchor(AnchorKind.END_STRING).to_pattern() == "\\Z"
    assert Anchor(AnchorKind.WORD_BOUNDARY).to_pattern() == "\\b"
    assert Anchor(AnchorKind.NON_WORD_BOUNDARY).to_pattern() == "\\B"
    assert Anchor(AnchorKind.START).fixed_length() == 0