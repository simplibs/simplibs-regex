# Outers
from ...base_class import Regex
from ...containers.Group import Group


def NAMED_GROUP(inner: Regex, name: str) -> Group:
    """Build a regex expression matching a named capturing group.

    Init Params:
        inner (Regex): The inner regex expression to be captured.
        name (str): The name assigned to the capturing group.

    Pattern:
        A capturing group with a specific name (`(?P<name>...)`).

    Example:
        pattern = NAMED_GROUP(DIGIT, "code")
        # Matches: captures decimal digit into group "code"
    """
    return Group(inner, name=name)