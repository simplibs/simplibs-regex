from .raise_no_nodes_error import raise_no_nodes_error
from .raise_param_invalid_type_error import raise_param_invalid_type_error
from .raise_param_not_identifier_error import raise_param_not_identifier_error


_DESIGN_NOTES = """
# Common Container Validations Sub-Package

## Purpose
Provides shared helper functions for validating general parameters and empty inputs in containers.

## Internal Components Registry

| Component                         | Type     | Description                                                                     |
| :-------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_no_nodes_error`            | Function | Raises a ParamError if the container is called with zero nodes[cite: 25].      |
| `raise_param_invalid_type_error`  | Function | Raises a ParamError if a container parameter has the wrong type[cite: 26].     |
| `raise_param_not_identifier_error`| Function | Raises a ParamError if the string parameter does not meet Python identifier rules[cite: 25]. |
"""