# Outers
from ...base_class import Regex
from ...containers.Group import Group


def NON_CAPTURING(inner: Regex) -> Group:
    """Build a regex expression matching a non-capturing group.

    Init Params:
        inner (Regex): The inner regex expression to group without capturing.

    Pattern:
        A group that controls precedence or flags without saving the matched text (`(?:...)`).

    Example:
        pattern = NON_CAPTURING(Sequence(Literal("a"), Literal("b")))
        # Matches: "ab" as a combined unit without creating a capture group
    """
    return Group(inner, capturing=False)