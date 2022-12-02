#!/usr/bin/env python
"""Convert toml to json."""
import json
import sys
from argparse import Namespace

from translate_shell import __version__

try:
    import tomlib  # type: ignore
except ImportError:
    import tomli as tomlib


with open(sys.argv[1], "rb") as f:
    project = Namespace(**tomlib.load(f)["project"])

data = {
    "name": project.name,
    "description": project.description,
    "version": __version__,
    "author": project.authors[0]["name"]
    + " <"
    + project.authors[0]["email"]
    + ">",
    "repository": {"type": "git", "url": project.urls["Source"]},
}
print(json.dumps(data))
