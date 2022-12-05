#!/usr/bin/env bash
for file in requirements/*.txt ; do
	filename="${file##*/}"
  cat "$file" | perl -pe's=^([^#]\S*)=- [\1](https://pypi.org/project/\1)=g;s/^#\s*//g;s/^!.*/## '"${filename%%.txt}"'/g'
done
