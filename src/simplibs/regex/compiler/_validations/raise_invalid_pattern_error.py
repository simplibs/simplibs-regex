import re

from simplibs.exception import ValidationError


def raise_invalid_pattern_error(
    node: object,
    pattern_string: str,
    err: re.error,
) -> None:
    """Raise a structured diagnostic when a fully-built Regex tree still
    fails to compile.

    This is the one failure Regex's own per-node construction-time
    validation cannot catch in isolation: every Group, Lookaround,
    Repeat, etc. validates its OWN parameters when built, but a
    cross-tree conflict — most commonly two Group(name=...) items
    sharing the same name at different points in the tree — only
    becomes visible once the whole pattern string exists and re.compile
    actually parses it as one piece.
    """
    raise ValidationError(
        error_name="REGEX_INVALID_PATTERN_ERROR",
        label="pattern",
        value=pattern_string,
        expected="a pattern tree that compiles to a syntactically valid regular expression",
        problem=(
            f"Compiling the pattern built from {node!r} produced "
            f"{pattern_string!r}, which failed: {err}"
        ),
        how_to_fix=(
            "This usually means two Group(name=...) items share the same "
            "name somewhere in the tree — a cross-tree conflict no single "
            "node's own construction-time validation could have caught in "
            "isolation. Check for duplicate group names."
        ),
        exception=re.error,
    ) from err