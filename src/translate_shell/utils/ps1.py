r"""PS1
=======

Generate a `powerlevel10k <https://github.com/romkatv/powerlevel10k>`_ -like
prompt for python.

Usage
~~~~~

Add the following code to your ``$PYTHONSTARTUP``:

..code:: python
    import sys

    from translate_shell.utils.ps1 import Ps1

    sys.ps1 = Ps1()
"""
import sys
from typing import Callable

from translate_shell.utils.misc import (
    p10k_sections,
    section_os,
    section_path,
    section_time,
)


class Ps1:
    """Ps1."""

    def __init__(
        self,
        prompt_string: str = "\n>>> ",
        sections: None
        | list[str | tuple[str, str, str | Callable[[], str]]] = None,
    ) -> None:
        """Init.

        :param prompt_string:
        :type prompt_string: str
        :param sections:
        :type sections: None
                | list[str | tuple[str, str, str | Callable[[], str]]]
        :rtype: None
        """
        insert_time = " {time}"

        self.prompt_string = prompt_string
        if sections is None:
            self.sections = [
                ("BLACK", "YELLOW", section_os()),
                (
                    "GREEN",
                    "BLACK",
                    f" {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                ),
                ("WHITE", "BLUE", section_path),
                (
                    "BLACK",
                    "WHITE",
                    lambda: insert_time.format(time=section_time()),
                ),
            ]
        else:
            self.sections = sections

    def __str__(self) -> str:
        """Str."""
        return p10k_sections(self.sections) + self.prompt_string  # type: ignore
