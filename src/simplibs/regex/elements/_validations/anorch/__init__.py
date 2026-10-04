from .raise_anchor_requires_python_314_error import raise_anchor_requires_python_314_error


_DESIGN_NOTES = """
# Anchor Validations Sub-Package

## Purpose
Provides structured functions for error reporting during anchor validations, including Python version support checks.

## Internal Components Registry

| Component                               | Type     | Description                                                                                        |
| :-------------------------------------- | :------- | :------------------------------------------------------------------------------------------------- |
| `raise_anchor_requires_python_314_error`| Function | Raises a ValidationError if AnchorKind.END_STRING_PY314 is used on a Python version older than 3.14. |
"""