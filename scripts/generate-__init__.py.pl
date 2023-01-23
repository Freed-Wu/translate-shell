#!/usr/bin/env -S perl -p
BEGIN {
  $name = shift;
  $name =~ s=.*/external/(.+?)/__init__\.py=$1=;
  $name =~ s=/=.=g;
}
s/shtab/$name/g;
$mark = "=" x length $name;
s/=====/$mark/;
