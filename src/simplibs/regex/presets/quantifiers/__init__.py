from .OPTIONAL import OPTIONAL
from .ZERO_OR_MORE import ZERO_OR_MORE
from .ONE_OR_MORE import ONE_OR_MORE
from .EXACTLY import EXACTLY
from .AT_LEAST import AT_LEAST
from .BETWEEN import BETWEEN


_DESIGN_NOTES = """
# Quantifiers Presets Sub-Package

## Purpose
Provides ergonomic quantifier builder helpers (`OPTIONAL`, `ZERO_OR_MORE`, `BETWEEN`, etc.) built on top of the underlying `Repeat` container.

## Components Registry

| Component       | Type   | Description                                           |
| :-------------- | :----- | :---------------------------------------------------- |
| `OPTIONAL`      | Preset | Matches zero or one occurrence (`...?`).              |
| `ZERO_OR_MORE`  | Preset | Matches zero or more occurrences (`...*`).            |
| `ONE_OR_MORE`   | Preset | Matches one or more occurrences (`...+`).             |
| `EXACTLY`       | Preset | Matches an exact count of repetitions (`...{n}`).     |
| `AT_LEAST`      | Preset | Matches a minimum count of repetitions (`...{n,}`).   |
| `BETWEEN`       | Preset | Matches a bounded range of repetitions (`...{m,n}`).  |
"""