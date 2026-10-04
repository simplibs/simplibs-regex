from .raise_node_not_regex_error import raise_node_not_regex_error


_DESIGN_NOTES = """
# Container Validations Sub-Package

## Purpose
Provides structured functions for error reporting during the validation of nodes passed into containers.

## Internal Components Registry

| Component                    | Type     | Description                                                                     |
| :--------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_node_not_regex_error` | Function | Raises a structured `ParamError` if a container element is not of type Regex.   |
"""