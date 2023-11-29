r"""REPL
========

Generate a `powerlevel10k <https://github.com/romkatv/powerlevel10k>`_ -like
prompt for python.
"""
import os
import sys
from contextlib import suppress

from .ps1 import Ps1


def interact(**kwargs: bool) -> None:
    """Interact.

    :param kwargs:
    :type kwargs: bool
    :rtype: None
    """
    from code import interact as _interact

    sys.ps1 = Ps1()

    if kwargs.get("wakatime", True) or kwargs.get("codestats", True):
        with suppress(ImportError):
            from repl_python_wakatime.python import install_hook

            if kwargs.get("wakatime", True):
                install_hook()

            if kwargs.get("codestats", True):
                from repl_python_wakatime.hooks.codestats import codestats_hook

                install_hook(codestats_hook)

    if kwargs.get("jedi", True):
        with suppress(ImportError):
            # Windows doesn't have readline
            import readline

            from jedi import settings
            from jedi.utils import setup_readline

            setup_readline()
            settings.add_bracket_after_function = True

    if kwargs.get("rich", True):
        with suppress(ImportError):
            import logging

            from rich import pretty, traceback
            from rich.logging import RichHandler

            pretty.install()
            traceback.install()
            logging.basicConfig(
                level=logging.WARNING,
                format="%(message)s",
                handlers=[RichHandler(rich_tracebacks=True, markup=True)],
            )

    if len(sys.argv) and os.path.basename(sys.argv[0]) == "__main__.py":
        _interact()
