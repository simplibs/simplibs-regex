from .START import START
from .END import END
from .START_STRING import START_STRING
from .END_STRING import END_STRING
from .WORD_BOUNDARY import WORD_BOUNDARY
from .NON_WORD_BOUNDARY import NON_WORD_BOUNDARY


_DESIGN_NOTES = """
# Anchors Presets Sub-Package

## Purpose
Provides zero-width position assertion presets (`START`, `END`, `WORD_BOUNDARY`, etc.) built on top of the underlying `Anchor` element.

## Components Registry

| Component             | Type   | Description                                           |
| :-------------------- | :----- | :---------------------------------------------------- |
| `START`               | Preset | Matches the start of a line (`^`).                    |
| `END`                 | Preset | Matches the end of a line (`$`).                      |
| `START_STRING`        | Preset | Matches the absolute start of the string (`\\A`).     |
| `END_STRING`          | Preset | Matches the absolute end of the string (`\\Z`).       |
| `WORD_BOUNDARY`       | Preset | Matches a word boundary (`\\b`).                      |
| `NON_WORD_BOUNDARY`   | Preset | Matches a non-word boundary (`\\B`).                  |
"""