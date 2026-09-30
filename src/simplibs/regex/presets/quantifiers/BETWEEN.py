# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat, RepeatMode


def BETWEEN(
    inner: Regex, min_count: int, max_count: int, *, mode: RepeatMode = RepeatMode.GREEDY
) -> Repeat:
    """Build a regex expression matching a bounded range of occurrences.

    Init Params:
        inner (Regex): The inner regex expression to repeat.
        min_count (int): The minimum number of repetitions (inclusive).
        max_count (int): The maximum number of repetitions (inclusive).
        mode (RepeatMode): The backtracking behavior (greedy, lazy, or possessive).

    Pattern:
        A bounded range of repetitions (`...{min_count,max_count}`).

    Example:
        pattern = BETWEEN(DIGIT, 2, 4)
        # Matches: "12", "123", "1234"
        # Does not match: "1", "12345"
    """
    return Repeat(inner, min=min_count, max=max_count, mode=mode)