r"""PS1
=======
"""
import sys
from typing import Callable

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
                ("BLACK", "YELLOW", section_os_icon()),
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
