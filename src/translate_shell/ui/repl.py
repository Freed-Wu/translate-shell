"""Read-eval-print Loop
=======================
"""
import os
import signal
from argparse import Namespace
from subprocess import check_output
from threading import Thread
from time import sleep

from . import init, process


def run_clipboard(args: Namespace) -> None:
    """Translate clipboard automatically.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    clipper = args.get_clipper()
    pid = os.getpid()
    if args.gui:
        from .gui import GUIPrint

        print_output = GUIPrint(args)
    else:
        print_output = print
    args.text = check_output(clipper, universal_newlines=True)
    args.last_text, _, _, _ = args.process_input(
        args.text, args.target_lang, args.source_lang, args.translators, False
    )
    while args.clipboard:
        sleep(args.sleep_seconds)
        args.text = check_output(clipper, universal_newlines=True)
        text, rst = process(args)
        if rst:
            args.last_text = text
            print(
                args.get_prompt(
                    args.text,
                    args.target_lang,
                    args.source_lang,
                    args.translators,
                )
            )
            print_output(rst, end="")
            os.kill(pid, signal.SIGINT)


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    args = init(args)
    task = Thread(target=run_clipboard, args=(args,))
    task.daemon = True
    task.start()
    while True:
        try:
            args.text = input(
                args.get_prompt(
                    "", args.target_lang, args.source_lang, args.translators
                )
            )
            _, rst = process(args, True)
            if rst:
                print(rst)
        except KeyboardInterrupt:
            # TODO: make the last line gray like ptpython
            print("")
            continue
        except EOFError:
            break
