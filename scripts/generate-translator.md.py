#!/usr/bin/env python
"""Generate translator.md."""
from translate_shell.translators import TRANSLATORS

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
