#!/usr/bin/env python
"""Generate ``CITATION.cff``."""
import sys

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

with open(sys.argv[1], "r") as f:
    citation = f.read()

with open(sys.argv[2], "rb") as f:
    project = tomllib.load(f)["project"]

print(
    citation.format(
        url=project["urls"]["Source"],
        name=project["name"],
        description=project["description"],
    ),
    end="",
)
