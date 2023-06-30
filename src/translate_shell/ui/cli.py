"""Command Line interface
=========================
"""
from argparse import Namespace

from . import process


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    process(args)
