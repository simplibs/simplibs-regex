from .LOOKAHEAD import LOOKAHEAD
from .NEGATIVE_LOOKAHEAD import NEGATIVE_LOOKAHEAD
from .LOOKBEHIND import LOOKBEHIND
from .NEGATIVE_LOOKBEHIND import NEGATIVE_LOOKBEHIND


_DESIGN_NOTES = """
# Lookaround Presets Sub-Package

## Purpose
Provides lookaround assertion helpers (`LOOKAHEAD`, `LOOKBEHIND`, and their negative variants) built on top of the underlying `Lookaround` container.

## Components Registry

| Component             | Type   | Description                                           |
| :-------------------- | :----- | :---------------------------------------------------- |
| `LOOKAHEAD`           | Preset | Positive lookahead assertion (`(?=...)`).             |
| `NEGATIVE_LOOKAHEAD`  | Preset | Negative lookahead assertion (`(?!...)`).             |
| `LOOKBEHIND`          | Preset | Positive lookbehind assertion (`(?<=...)`).           |
| `NEGATIVE_LOOKBEHIND` | Preset | Negative lookbehind assertion (`(?<!...)`).           |
"""