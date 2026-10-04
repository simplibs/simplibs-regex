from .flatten_nodes import flatten_nodes


_DESIGN_NOTES = """
# Container Helpers Sub-Package

## Purpose
Contains helper functions for processing, flattening, and validating nodes within containers, such as Alternation and Sequence.

## Internal Components Registry

| Component       | Type     | Description                                                                     |
| :-------------- | :------- | :------------------------------------------------------------------------------ |
| `flatten_nodes` | Function | Flattens nested container instances and verifies that all items are valid Regex nodes. |
"""