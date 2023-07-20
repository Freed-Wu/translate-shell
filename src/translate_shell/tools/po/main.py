r"""Refer ``action.yml``."""
import logging
import os
from argparse import Namespace
from difflib import Differ
from glob import glob

from polib import pofile
from tqdm import tqdm

from translate_shell.translate import translate

try:
    import tomllib as tomli
except ImportError:
    import tomli

logger = logging.getLogger(__name__)


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    fnames = args.files
    default_target_lang = args.target_lang
    source_lang = args.source_lang
    translator = args.translator
    option = tomli.loads("\n".join(args.option))
    wrapwidth = int(args.wrapwidth)
    progress = args.progress.lower() == "true"
    verbose = args.verbose.lower() == "true"
    dry_run = args.dry_run.lower() == "true"
    force = args.force.lower() == "true"
    workspace = args.workspace

    differ = Differ()
    files = sum(
        [
            glob(os.path.join(workspace, fname), recursive=True)
            for fname in fnames.splitlines()
        ],
        [],
    )
    for file in files:
        po = pofile(file, wrapwidth=wrapwidth)
        target_lang = po.metadata.get("Language")
        if not target_lang:
            target_lang = default_target_lang
        entries = po.untranslated_entries()
        if force:
            entries += po.translated_entries()
        print(f"{po.fpath}: {len(entries)}")
        if dry_run:
            continue
        if progress:
            entries = tqdm(entries)
        for entry in entries:
            old = str(entry).splitlines()
            try:
                entry.msgstr = translate(
                    entry.msgid,
                    target_lang,
                    source_lang,
                    [translator],
                    {translator: option},
                ).results[0]["paraphrase"]
            except Exception as e:  # skipcq: PYL-W0703
                logger.warning(e)
                po.save()
                continue
            entry.fuzzy = False  # type: ignore
            if verbose:
                new = str(entry).splitlines()
                diff = differ.compare(old, new)
                print("\n".join(diff))
        if len(entries):
            po.save()
