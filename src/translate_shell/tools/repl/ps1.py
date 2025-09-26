r"""PS1
=======
"""

import asyncio
import sys
from collections.abc import Callable, Coroutine, Iterable
from dataclasses import dataclass

from ...utils.section import (
    p10k_sections,
    section_os_icon,
    section_path,
    section_time,
)


@dataclass
class Ps1:
    """Ps1."""

    prompt_string: str = "\n>>> "
    sections: Iterable[str | tuple[str, str, str | Callable[[], str]]] = (
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
            lambda: f" {section_time()}",
        ),
    )
    hook: Coroutine | None = None

    def __str__(self) -> str:
        """Str."""
        if self.hook:
            asyncio.run(self.hook)
        return p10k_sections(self.sections) + self.prompt_string
