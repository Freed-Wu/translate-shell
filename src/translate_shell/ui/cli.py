"""Command Line interface
=========================
"""
from argparse import Namespace

from . import init, process


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    args = init(args)
    args.last_text, rst = process(args)
    print(rst)
