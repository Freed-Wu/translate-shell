"""Read-eval-print Loop
=======================
"""
import os
import signal
from argparse import Namespace
from copy import deepcopy
from subprocess import check_output
from threading import Thread
from time import sleep

from . import init, init_readline, process


def process_clipboard(args: Namespace) -> None:
    """Process clipboard.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    clipper = args.get_clipper()
    pid = os.getpid()
    args.text = check_output(clipper, universal_newlines=True)
    args.last_text, _, _, _ = args.process_input(
        args.text, args.target_lang, args.source_lang, args.translators, False
    )
    global stop, is_enable_clipboard
    while not stop:
        sleep(0.1)
        args.text = check_output(clipper, universal_newlines=True)
        text, rst = process(args)
        if rst and is_enable_clipboard:
            args.last_text = text
            print(
                args.get_prompt(
                    args.text,
                    args.target_lang,
                    args.source_lang,
                    args.translators,
                )
            )
            print(rst)
            os.kill(pid, signal.SIGINT)


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    global stop, is_enable_clipboard
    stop = False
    is_enable_clipboard = args.clipboard
    args = init(args)
    # for CLI and clipboard, last_text is "" or a string.
    # We can use last_text is None to judge if we are in REPL
    args.last_text = None
    init_readline()
    _args = deepcopy(args)
    task = Thread(target=process_clipboard, args=(_args,))
    task.start()
    while True:
        try:
            args.text = input(
                args.get_prompt(
                    "", args.target_lang, args.source_lang, args.translators
                )
            )
            _, rst = process(args)
            print(rst, end="\n" if rst else "")
        except KeyboardInterrupt:
            # TODO: make the last line gray like ptpython
            print("")
            continue
        except EOFError:
            break
    stop = True
