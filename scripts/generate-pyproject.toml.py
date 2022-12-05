#!/usr/bin/env python
"""Update pyproject.toml from ``requirements/*.txt``."""
import os
import sys

import tomli_w

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

with open(sys.argv[1], "rb") as f:
    data = tomllib.load(f)

requirements = {}
for dirname, j, k in os.walk("requirements"):
    for filename in k:
        requirements[filename.split(".")[0]] = {
            "file": os.path.join(dirname, filename)
        }
dynamic = {}
dynamic["optional-dependencies"] = requirements
data["tool"]["setuptools"]["dynamic"] = dynamic
print(tomli_w.dumps(data), end="")
