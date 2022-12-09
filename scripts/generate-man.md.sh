#!/usr/bin/env bash
cd "$(dirname "$(dirname "$0")")" || exit 1
help2man scripts/trans | pandoc -fman -tmarkdown --shift-heading-level-by=1 |
	perl -pe's/\\<(\S+)\\>/[<\1>](mailto:\1)/g;s=(https://\S+)=<\1>=g;
	s=(\S+)\((\d)\)=[\1(\2)](https://www.unix.com/man-page/debian/\2/\1/)=g;
	s/\\--/----/g;s/trans (\*\*)?----print-setting(\*\*)?/trans --print-setting/g'
