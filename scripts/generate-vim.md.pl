#!/usr/bin/env -S perl -n
$i++ if /===/;
next if $i < 2 or /^vim:/;
s/^:/\\:/;
s/={3,}\n/## /;
s/\s{2,}\*(\S+)\*$/\n\n### $1/;
s/\s*`$//;
print;
