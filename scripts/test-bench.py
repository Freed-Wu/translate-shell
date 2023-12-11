#!/usr/bin/env python
r"""Test bench
==============

.. code:: sh

    $ ./test_bench.py --translators=google,bing,haici,stardict block

    input text:     block
    target lang     zh_CN
    source lang:    auto
    translators:    google,bing,haici,stardict

    coroutine:
            time:    1.8392638560035266
            results:         4
    threading:
            time:    0.6133544620242901
            results:         4
    serial run:
            time:    1.6182543189497665
            results:         4
"""
import time
from timeit import timeit

from translate_shell.__main__ import get_parser
from translate_shell.translate import translate
from translate_shell.ui import init

NUMBER = 1
SLEEP_SECONDS = 0.5

parser = get_parser()
args = parser.parse_args()
init(args)
print(
    f"""
input text:\t{args.text}
target lang\t{args.target_lang}
source lang:\t{args.source_lang}
translators:\t{args.translators}
"""
)
args.translators = args.translators.split(",")

translationss = {}
for use in ["coroutine", "threading", "serial run"]:
    print(
        f"{use}:\n\ttime:\t",
        timeit(
            f"""
translationss[{use!r}] = translate(
    args.text,
    args.target_lang,
    args.source_lang,
    args.translators,
    use={use!r},
)
""",
            globals=globals(),
            number=NUMBER,
        ),
    )
    # avoid anti spider
    time.sleep(SLEEP_SECONDS)
    print("\tresults:\t", len(translationss[use].results))
