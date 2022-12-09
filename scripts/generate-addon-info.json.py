#!/usr/bin/env python
"""Convert pyproject.toml to addon-info.json."""
import json
import sys
from argparse import Namespace

from translate_shell import __version__  # type: ignore

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib  # type: ignore


with open(sys.argv[1], "rb") as f:
    project = Namespace(**tomllib.load(f)["project"])

data = {
    "name": project.name,
    "description": project.description,
    "version": __version__.partition(".dev")[0],
    "author": project.authors[0]["name"]
    + " <"
    + project.authors[0]["email"]
    + ">",
    "repository": {"type": "git", "url": project.urls["Source"]},
}
print(json.dumps(data))
