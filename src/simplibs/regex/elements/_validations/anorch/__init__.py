from .raise_anchor_invalid_kind_error import raise_anchor_invalid_kind_error

_DESIGN_NOTES = """
# Anchor Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Anchor validation.

## Internal Components Registry

| Component                       | Type     | Description                                                                     |
| :------------------------------ | :------- | :------------------------------------------------------------------------------ |
| `raise_anchor_invalid_kind_error` | Function | Emits structured `ParamError` when an invalid AnchorKind is received.          |
"""