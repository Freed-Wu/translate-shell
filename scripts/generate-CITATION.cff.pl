#!/usr/bin/env -S perl -pi
unless ($#ARGV < 0) {
  $name = $1 if /^name = "([^"]*+)"/;
  $description = $1 if /^description = "([^"]*+)"/;
  $url = $1 if /^Source = "([^"]*+)"/;
  next;
};
s/(?<=^title: ")([^"]*+)(?="$)/$name: $description/;
s/(?<=^url: ")([^"]*+)(?="$)/$url/;
