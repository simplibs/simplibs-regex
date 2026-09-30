# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat


def OPTIONAL(inner: Regex) -> Repeat:
    """Build a regex expression matching zero or one occurrence of the inner pattern.

    Init Params:
        inner (Regex): The inner regex expression to make optional.

    Pattern:
        Zero or one occurrence of the inner node (`...?`).

    Example:
        pattern = OPTIONAL(Literal("s"))
        # Matches: "s" or an empty string
    """
    return Repeat(inner, min=0, max=1)