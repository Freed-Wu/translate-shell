#!/usr/bin/env python
r"""Refer ``action.yml``."""
import os
from difflib import Differ
from glob import glob

import polib
from tqdm import tqdm

from translate_shell.translate import translate

fnames = os.getenv("INPUT_FILES", "**/*.po")
default_target_lang = os.getenv("INPUT_TARGET_LANG", "zh-cn")
source_lang = os.getenv("INPUT_SOURCE_LANG", "en")
translator = os.getenv("INPUT_TRANSLATOR", "google")
wrapwidth = int(os.getenv("INPUT_WRAPWIDTH", "76"))
progress = os.getenv("INPUT_PROGRESS", "true").lower() == "true"
verbose = os.getenv("INPUT_PROGRESS", "false").lower() == "true"
dry_run = os.getenv("INPUT_DRY_RUN", "false").lower() == "true"

workspace = os.getenv("GITHUB_WORKSPACE", ".")
differ = Differ()
files = sum(
    [
        glob(os.path.join(workspace, fname), recursive=True)
        for fname in fnames.splitlines()
    ],
    [],
)

for file in files:
    po = polib.pofile(file, wrapwidth=wrapwidth)
    target_lang = po.metadata.get("Language", "en")
    untranslated_entries = po.untranslated_entries()
    print(f"{po.fpath}: {len(untranslated_entries)}")
    if dry_run:
        continue
    if progress:
        untranslated_entries = tqdm(untranslated_entries)
    for entry in untranslated_entries:
        old = str(entry).splitlines()
        try:
            entry.msgstr = translate(
                entry.msgid, target_lang, source_lang, [translator]
            ).results[0]["paraphrase"]
        except Exception:
            po.save()
            continue
        entry.fuzzy = False  # type: ignore
        if verbose:
            new = str(entry).splitlines()
            diff = differ.compare(old, new)
            print("\n".join(diff))
    if len(untranslated_entries):
        po.save()
