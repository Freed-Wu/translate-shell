"""Command Line interface
=========================
"""
from argparse import Namespace

from . import init, init_readline, process


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    args = init(args)
    readline = init_readline()
    readline.add_history(args.text)
    _, rst = process(args)
    print(rst)
