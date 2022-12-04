#!/usr/bin/env python
"""Convert pyproject.toml to version.txt."""
import sys
from datetime import datetime

from setuptools_scm import get_version

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

copyright = "2022-" + str(datetime.now().year)
version = get_version().partition(".dev")[0]

with open(sys.argv[1], "rb") as f:
    author = tomllib.load(f)["project"]["authors"][0]["name"]

with open(sys.argv[2], "r") as f:
    print(
        f.read().format(version=version, author=author, copyright=copyright),
        end="",
    )
