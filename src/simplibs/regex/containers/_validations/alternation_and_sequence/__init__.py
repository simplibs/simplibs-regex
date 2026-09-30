from .raise_node_param_not_regex_error import raise_node_param_not_regex_error
from .raise_requires_at_least_one_node_error import raise_requires_at_least_one_node_error

_DESIGN_NOTES = """
# Alternation and Sequence Validations Sub-Package

## Purpose
Provides structured exception emission helpers for alternation and sequence container validation.

## Internal Components Registry

| Component                               | Type     | Description                                                                     |
| :-------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_node_param_not_regex_error`      | Function | Emits structured `ParamError` when a provided node is not a Regex instance.    |
| `raise_requires_at_least_one_node_error`| Function | Emits structured `ParamError` when a container receives no nodes.             |
"""