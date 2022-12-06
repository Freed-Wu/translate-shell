#!/usr/bin/env python
"""Generate ``src/*/external/*/__init__.py``."""
import os
import sys

name = os.path.dirname(sys.argv[1]).split("external/")[-1].replace("/", ".")
char = "="
head = '"""Fake '
with open(sys.argv[2]) as f:
    print(
        f.read()
        .replace("__init__", name)
        .replace(char * len(head + "__init__"), char * len(head + name)),
        end="",
    )
