from typing import Any, Iterable, Type
# Outers
from ...base_class import Regex
# Inners
from .validations import raise_node_not_regex_error


def flatten_nodes(
    nodes: Iterable[Any],
    container_type: Type[Any],
    caller_name: str,
) -> list[Regex]:
    """Flatten nested container instances and validate that all items are Regex nodes.

    Args:
        nodes: The raw input nodes passed to the container constructor.
        container_type: The exact container class type to unwrap (e.g., Alternation, Sequence).
        caller_name: Name of the caller container (used for error reporting).

    Returns:
        A flat list of validated Regex nodes.

    Raises:
        ParamError: If any node is not an instance of Regex.
    """

    # 1. Initialize the accumulator list for the flattened and validated nodes.
    flattened: list[Regex] = []

    # 2. Iterate through all provided raw input nodes.
    for node in nodes:

        # 2.1 Validate that every item is a proper Regex instance.
        if not isinstance(node, Regex):
            raise_node_not_regex_error(caller_name, node)

        # 2.2 If the node is an exact instance of the container type, unwrap and extend its nodes.
        if type(node) is container_type:
            # noinspection PyUnresolvedReferences
            flattened.extend(node.nodes)

        # 2.3 Otherwise, append the single node directly.
        else:
            flattened.append(node)

    # 3. Return the fully flattened and validated list of regex nodes.
    return flattened


_DESIGN_NOTES = """
# flatten_nodes — Shared Container Node Flattening Helper

## Purpose
Centralizes the node-flattening and validation logic shared by container classes
such as `Alternation` and `Sequence`. Eliminates code duplication while preserving
exact-type unwrap semantics (`type(node) is container_type`).

---

## 1. Execution Rationale

* **Exact-Type Unwrapping:**
  Uses `type(node) is container_type` rather than `isinstance` to ensure that
  deliberate subclasses with custom behavior are never silently unwrapped.
* **Fail-Fast Validation:**
  Every element is strictly checked via `isinstance(node, Regex)` before any
  unwrapping occurs, raising a structured diagnostic error immediately if invalid.
"""