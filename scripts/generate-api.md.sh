#!/usr/bin/env bash
# shellcheck disable=SC2086
cd "$(dirname "$(dirname "$0")")" || exit 1
find src/translate_shell/$1 $2 $3 -name '*.py' |
	perl -pe's=src/=.. automodule:: =g;s=\.py$=\n    :members:=g;
	s=/__init__==g;s=/=.=g'
