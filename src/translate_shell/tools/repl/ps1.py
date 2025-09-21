r"""PS1
=======
"""

import sys
from collections.abc import Callable, Iterable

from ...utils.section import (
    p10k_sections,
    section_os_icon,
    section_path,
    section_time,
)


class Ps1:
    """Ps1."""

    def __init__(
        self,
        prompt_string: str = "\n>>> ",
        sections: None
        | Iterable[str | tuple[str, str, str | Callable[[], str]]] = None,
        hook: Callable = lambda: None,
    ) -> None:
        """Init.

        :param prompt_string:
        :type prompt_string: str
        :param sections:
        :type sections: None
                | Iterable[str | tuple[str, str, str | Callable[[], str]]]
        :param hook:
        :type hook: Callable
        :rtype: None
        """
        self.hook = hook
        insert_time = " {time}"

        self.prompt_string = prompt_string
        if sections is None:
            self.sections = [
                ("BLACK", "YELLOW", section_os_icon()),
                (
                    "GREEN",
                    "BLACK",
                    f" {sys.version_info.major}.{sys.version_info.minor}."
                    f"{sys.version_info.micro}",
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
        self.hook()
        return p10k_sections(self.sections) + self.prompt_string
