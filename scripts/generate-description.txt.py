#!/usr/bin/env python
"""Convert pyproject.toml to description.txt."""
import sys

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

with open(sys.argv[1], "rb") as f:
    description = tomllib.load(f)["project"]["description"]

print(description)
