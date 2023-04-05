"""Graphics User Interface
==========================
"""
from argparse import Namespace
from subprocess import check_output
from time import sleep

from . import process


def run(args: Namespace) -> None:
    """Translate clipboard automatically.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    clipper = args.get_clipper()
    if clipper == []:
        return None
    args.text = check_output(clipper, universal_newlines=True)
    args.last_text, _, _, _ = args.process_input(
        args.text, args.target_lang, args.source_lang, args.translators, False
    )
    while True:
        sleep(args.sleep_seconds)
        args.text = check_output(clipper, universal_newlines=True)
        process(args)
