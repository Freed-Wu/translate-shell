#!/usr/bin/env python
r"""Refer ``action.yml``."""
import os
from difflib import Differ
from glob import glob

import polib

from translate_shell.translate import translate

fnames = os.getenv("INPUT_FILES", "**/*.po")
default_target_lang = os.getenv("INPUT_TARGET_LANG", "zh-cn")
source_lang = os.getenv("INPUT_SOURCE_LANG", "en")
translator = os.getenv("INPUT_TRANSLATOR", "google")
wrapwidth = int(os.getenv("INPUT_WRAPWIDTH", "76"))

workspace = os.getenv("GITHUB_WORKSPACE", ".")
differ = Differ()
files = sum(
    [
        glob(os.path.join(workspace, fname), recursive=True)
        for fname in fnames.splitlines()
    ],
    [],
)
pos = [polib.pofile(file, wrapwidth=wrapwidth) for file in files]

for po in pos:
    target_lang = po.metadata.get("Language", "en")
    untranslated_entries = po.untranslated_entries()
    print(f"{po.fpath}: {len(untranslated_entries)}")
    for entry in untranslated_entries:
        old = str(entry).splitlines()
        entry.msgstr = translate(
            entry.msgid, target_lang, source_lang, [translator]
        ).results[0]["paraphrase"]
        entry.fuzzy = False  # type: ignore
        new = str(entry).splitlines()
        diff = differ.compare(old, new)
        print("\n".join(diff))
    if len(untranslated_entries):
        po.save()
