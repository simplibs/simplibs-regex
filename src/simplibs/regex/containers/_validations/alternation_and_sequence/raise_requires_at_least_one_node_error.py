from typing import NoReturn
from simplibs.exception import ValidationError


def raise_requires_at_least_one_node_error(container_name: str) -> NoReturn:
    """Raise a structured ValidationError when a container is constructed with zero nodes."""
    raise ValidationError(
        error_name="CONTAINER_REQUIRES_NODES",
        label=f"{container_name} nodes",
        value=0,
        problem=(
            f"{container_name}() requires at least one node — got none.",
            "Containers like Alternation or Sequence cannot be empty as they require child expressions to form a valid pattern fragment.",
        ),
        expected="At least one valid Regex instance passed as a positional argument.",
        how_to_fix=(
            f"Pass one or more Regex nodes into {container_name}().",
            "Ensure that dynamic node lists are not empty before constructing the container.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_requires_at_least_one_node_error — Container Node Count Validation

## Purpose
Enforces that container structures (`Alternation`, `Sequence`, etc.) receive at least 
one node upon initialization, preventing empty or meaningless composite expressions.
"""