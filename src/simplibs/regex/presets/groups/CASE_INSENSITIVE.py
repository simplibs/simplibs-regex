from ...base_class import Regex
from ...containers.Group import Group
from ...flags.Flag import Flag

def CASE_INSENSITIVE(inner: Regex) -> Group:
    """Build a regex expression matching `inner` with case-insensitive matching.

    Init Params:
        inner (Regex): The inner regex expression the flag applies to.

    Pattern:
        A non-capturing group with the `IGNORECASE` flag scoped to `inner` only (`(?i:...)`).

    Example:
        pattern = CASE_INSENSITIVE(Literal("ab"))
        # Matches: "ab", "AB", "aB"
    """
    return Group(inner, capturing=False, flags=frozenset({Flag.IGNORECASE}))
