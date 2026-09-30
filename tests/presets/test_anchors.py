from simplibs.regex.presets.anchors import (
    START,
    END,
    START_STRING,
    END_STRING,
    WORD_BOUNDARY,
    NON_WORD_BOUNDARY,
)

def test_anchor_presets():
    """Verify that anchor presets produce the correct patterns."""
    assert START.to_pattern() == "^"
    assert END.to_pattern() == "$"
    assert START_STRING.to_pattern() == "\\A"
    assert END_STRING.to_pattern() == "\\Z"
    assert WORD_BOUNDARY.to_pattern() == "\\b"
    assert NON_WORD_BOUNDARY.to_pattern() == "\\B"