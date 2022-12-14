#!/usr/bin/env bash
cd "$(dirname "$(dirname "$0")")" || exit 1
head -n-1 doc/translate-shell.txt | tail -n+4 | perl -p0777 -e's/={3,}.*?\n\n//s' | perl -pe's/^:/\\:/;s/={3,}\n/## /;s/\s{2,}\*(\S+)\*$/\n\n### \1/;s/\s*`$//'
