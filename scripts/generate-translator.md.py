#!/usr/bin/env python
"""Generate translator.md."""
import logging

from translate_shell.translators import TRANSLATORS

logging.basicConfig(level="CRITICAL")

print(
    "\n".join(
        "- [{k}]({v})".format(
            k=k,
            v=v().__class__.__module__.replace(
                "builtins", "translate_shell.translators"
            ),
        )
        for k, v in TRANSLATORS.items()
    )
)
