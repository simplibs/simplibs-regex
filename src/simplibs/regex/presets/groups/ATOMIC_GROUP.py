# Outers
from ...base_class import Regex
from ...containers.Group import Group


def ATOMIC_GROUP(inner: Regex) -> Group:
    """Build a regex expression matching an atomic group.

    Init Params:
        inner (Regex): The inner regex expression to evaluate atomically.

    Pattern:
        An independent sub-expression that prevents backtracking once matched (`(?>...)`).

    Example:
        pattern = ATOMIC_GROUP(Sequence(DIGIT, DIGIT))
        # Matches: two digits, discarding intermediate backtracking states
    """
    return Group(inner, atomic=True)