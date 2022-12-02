#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if any fake module imports any variable don't owned by any true module.
"""
import os
from importlib import import_module
from pathlib import Path
from typing import Any, NoReturn, _SpecialForm

from setuptools import find_packages


def filter_var(variables: dict[str, Any]) -> dict[str, Any]:
    """filter_var.

    :param variables:
    :type variables: dict[str, Any]
    :rtype: dict[str, Any]
    """
    return dict(
        filter(
            lambda x: not x[0].startswith("_")
            and not isinstance(x[1], _SpecialForm),
            variables.items(),
        )
    )


def get_wrong_varnames(file: str, fake_vars: dict[str, Any]) -> list[str]:
    """get_wrong_varnames.

    :param file:
    :type file: str
    :param fake_vars:
    :type fake_vars: dict[str, Any]
    :rtype: list[str]
    """
    true_vars = vars(import_module(Path(file).absolute().parent.name))
    true_vars = filter_var(true_vars)
    fake_vars = filter_var(fake_vars)

    wrong_varnames = []
    for varname in fake_vars:
        if varname not in true_vars:
            wrong_varnames += [varname]
    return wrong_varnames


def print_wrong_varnames(
    file: str, fake_vars: dict[str, Any], end: str = "\n"
) -> int:
    """print_wrong_varnames.

    :param file:
    :type file: str
    :param fake_vars:
    :type fake_vars: dict[str, Any]
    :param end:
    :type end: str
    :rtype: int
    """
    wrong_varnames = get_wrong_varnames(file, fake_vars)
    print(" ".join(wrong_varnames), end=end)
    return len(wrong_varnames)


def main_once(file: str, fake_vars: dict[str, Any]) -> NoReturn:
    """``python -m translate_shell.external.XXX`` call this function.

    :param file:
    :type file: str
    :param fake_vars:
    :type fake_vars: dict[str, Any]
    :rtype: NoReturn
    """
    exit(print_wrong_varnames(file, fake_vars, ""))


def main() -> NoReturn:
    """``python -m translate_shell.external`` call this function.

    :rtype: NoReturn
    """
    wrong_vars_number = 0
    for name in find_packages(os.path.dirname(__file__)):
        fake_name = "translate_shell.external." + name
        print(fake_name, end=": ")
        module = import_module(fake_name + ".__main__")
        file: str = module.__file__  # type: ignore
        wrong_vars_number += print_wrong_varnames(file, vars(module))
    exit(wrong_vars_number)


if __name__ == "__main__":
    main()
