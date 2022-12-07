#!/usr/bin/env -S perl -p0777
s/```\{eval-sh\}\n(.*)\n```\n/my $x = qx%$1%; chomp $x; $x/ge
