from ...base_class import Regex
from ...containers.Group import Group
from ...flags.Flag import Flag

def VERBOSE_GROUP(inner: Regex) -> Group:
    """Build a regex expression matching `inner` in verbose mode.

    Init Params:
        inner (Regex): The inner regex expression the flag applies to.

    Pattern:
        A non-capturing group with the `VERBOSE` flag scoped to `inner` only (`(?x:...)`).
        Whitespace and `#` of a `Literal` inside are escaped, so verbose mode
        never swallows them.

    Example:
        pattern = VERBOSE_GROUP(Literal("a b"))
        # Matches: "a b" (the escaped space is kept)
    """
    return Group(inner, capturing=False, flags=frozenset({Flag.VERBOSE}))
