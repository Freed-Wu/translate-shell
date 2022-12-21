#!/usr/bin/env -S perl -p
BEGIN {
  $name = shift;
  $name =~ s=.*/(.+?)/__init__\.py=$1=;
}
s/shtab/$name/g;
$mark = "=" x length $name;
s/=====/$mark/;
