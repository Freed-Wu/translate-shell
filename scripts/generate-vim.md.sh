#!/usr/bin/env bash
head -n-1 doc/translate-shell.txt | tail -n+4 | perl -0pe's/={3,}.*?\n\n//s' | perl -pe's/^:/\\:/;s/={3,}\n/## /;s/\s{2,}\*(\S+)\*$/\n### \1/;s/\s*`$//' | pandoc -fmarkdown -tmarkdown
