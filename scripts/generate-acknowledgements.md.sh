#!/usr/bin/env bash
cd "$(dirname "$(dirname "$0")")" || exit 1
grep -RIn Refer src | perl -pe's/:/#L/;s/:/  /;
s=^=- https://github.com/Freed-Wu/tranlate-shell/tree/main/=g;
s=(https://\S+)=<\1>=g;s=^(- \S+)=\1\n=g'
