#!/usr/bin/env python
"""Convert pyproject.toml to epilog.txt."""
import sys

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib


with open(sys.argv[1], "rb") as f:
    bug = tomllib.load(f)["project"]["urls"]["Bug Report"]

with open(sys.argv[2], "r") as f:
    print(f.read().format(bug=bug), end="")
