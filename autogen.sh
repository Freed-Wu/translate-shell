#!/usr/bin/env sh
# generate _version.py for AC_INIT
# and generate wheel for make install-data-local
python -m build -w
autoreconf -vif
