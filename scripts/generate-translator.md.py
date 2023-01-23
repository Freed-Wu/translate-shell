#!/usr/bin/env python
"""Generate translator.md."""
import logging

from translate_shell.translators import TRANSLATORS

# disable any error about unimplemented modules
logging.basicConfig(level="CRITICAL")

STRING = "translate_shell.translators"
print(
    "\n".join(
        f"- [{k}]({v().__class__.__module__.replace('builtins', STRING)})"
        for k, v in TRANSLATORS.items()
    )
)
