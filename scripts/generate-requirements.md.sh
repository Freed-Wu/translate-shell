#!/usr/bin/env bash
cd "$(dirname "$(dirname "$0")")" || exit 1
for file in requirements/*.txt; do
	filename="${file##*/}"
	perl -pe's=^([^#\n]\S*)=- [\1](https://pypi.org/project/\1)=g;s/^#\s*//g;s/^!.*/## '"${filename%%.txt}"'/g' <"$file"
done
