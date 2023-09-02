"""Read-eval-print Loop
=======================
"""
from argparse import Namespace
from threading import Thread

from . import process


def run(args: Namespace) -> None:
    """Run.

    .. todo::
        make the last line gray like ``ptpython``.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    if args.clipboard:
        from .gui import run as _run

        task = Thread(target=_run, args=(args,))
        task.daemon = True
        task.start()
    while True:
        try:
            args.text = input(
                args.get_prompt(
                    "", args.target_lang, args.source_lang, args.translators
                )
            )
            process(args, True)
        except KeyboardInterrupt:
            print("")
            continue
        except EOFError:
            break
