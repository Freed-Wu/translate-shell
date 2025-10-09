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

    def hook():
        pass

    with suppress(ImportError):
        from repl_python_wakatime.backends.chainedhook import ChainedHook
        from repl_python_wakatime.backends.codestats import CodeStats
        from repl_python_wakatime.backends.wakatime import Wakatime

        if kwargs.get("wakatime", True) and kwargs.get("codestats", True):
            hook = ChainedHook(hooks=(CodeStats(), Wakatime()))
        elif kwargs.get("wakatime", True):
            hook = Wakatime()
        elif kwargs.get("codestats", True):
            hook = CodeStats()

    sys.ps1 = Ps1(hook=hook)

    if kwargs.get("jedi", True):
        with suppress(ImportError):
            # Windows doesn't have readline
            import readline  # noqa: F401

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
