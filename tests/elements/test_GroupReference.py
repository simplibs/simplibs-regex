from simplibs.regex.elements.GroupReference import GroupReference

def test_group_reference():
    """Verify GroupReference patterns and fixed length (None)."""
    assert GroupReference(1).to_pattern() == "\\1"
    assert GroupReference("year").to_pattern() == "(?P=year)"
    assert GroupReference(1).fixed_length() is None