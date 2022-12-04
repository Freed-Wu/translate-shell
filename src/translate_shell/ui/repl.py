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


def translate_clipboard() -> None:
    """Translate clipboard automatically.

    :rtype: None
    """
    global args
    clipper = args.get_clipper()
    pid = os.getpid()
    args.text = check_output(clipper, universal_newlines=True)
    args.last_text, _, _, _ = args.process_input(
        args.text, args.target_lang, args.source_lang, args.translators, False
    )
    while not args.stop_clipboard:
        sleep(args.sleep_seconds)
        args.text = check_output(clipper, universal_newlines=True)
        text, rst = process(args)
        if rst and args.clipboard:
            args.last_text = text
            print(
                args.get_prompt(
                    args.text,
                    args.target_lang,
                    args.source_lang,
                    args.translators,
                )
            )
            print(rst, end="")
            os.kill(pid, signal.SIGINT)


def run(input_args: Namespace) -> None:
    """Run.

    :param input_args:
    :type input_args: Namespace
    :rtype: None
    """
    global args
    args = init(input_args)
    task = Thread(target=translate_clipboard, args=())
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
    args.stop_clipboard = True
