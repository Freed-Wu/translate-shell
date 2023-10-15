#!/usr/bin/env python
r"""Setup
=========
"""
from setuptools import setup

with open("action.yml") as fin, open(
    "src/translate_shell/tools/po/action.yml", "w"
) as fout:
    fout.write(fin.read())

setup()
