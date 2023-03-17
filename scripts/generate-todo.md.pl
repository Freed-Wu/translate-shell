#!/usr/bin/env -S perl -n
$.       = 1 unless $#ARGV == $oldargc;
$oldargc = $#ARGV;
next unless s/\s*#?\s*TODO:\s*//;
$label = $ARGV;
$label =~ s=.*?src/.*?/==;
s=(https://\S+)=<$1>=g;
print
"- [$label:$.](https://github.com/Freed-Wu/translate-shell/tree/main/$ARGV#L$.): $_";
