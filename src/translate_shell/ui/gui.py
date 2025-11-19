"""Graphics User Interface
==========================
"""

from argparse import Namespace
from time import sleep

import clipman

from . import process

clipman.init()


def run(args: Namespace) -> None:
    """Translate clipboard automatically.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    args.text = clipman.get()
    args.last_text, _, _, _ = args.process_input(
        args.text, args.target_lang, args.source_lang, args.translators, False
    )
    while True:
        sleep(args.sleep_seconds)
        args.text = clipman.get()
        process(args)
