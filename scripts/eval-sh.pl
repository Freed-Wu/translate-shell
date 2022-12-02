#!/usr/bin/env -S perl -0p
s/```\{eval-sh\}\n(.*)\n```\n/my $x = qx%$1%; \ chomp $x; $x/ge
