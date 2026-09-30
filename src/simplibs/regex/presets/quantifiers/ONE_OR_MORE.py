# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat, RepeatMode


def ONE_OR_MORE(inner: Regex, *, mode: RepeatMode = RepeatMode.GREEDY) -> Repeat:
    """Build a regex expression matching one or more occurrences of the inner pattern.

    Init Params:
        inner (Regex): The inner regex expression to repeat.
        mode (RepeatMode): The backtracking behavior (greedy, lazy, or possessive).

    Pattern:
        One or more occurrences of the inner node (`...+`).

    Example:
        pattern = ONE_OR_MORE(DIGIT)
        # Matches: "5", "12345"
        # Does not match: ""
    """
    return Repeat(inner, min=1, max=None, mode=mode)