#!/usr/bin/env bash
cat src/*/_version.py <(echo 'print(__version__)') | python
