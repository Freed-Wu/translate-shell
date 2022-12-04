#!/usr/bin/env python
"""Generate screenshot for REPL."""
from time import sleep

import pexpect

# wait 0.1s for zsh prompt string display firstly
# wait 0.2s for trans translate word
child = pexpect.spawn("zsh", encoding="utf-8")
sleep(0.1)
child.sendline("trans")
sleep(0.2)
child.sendline("en:ja")
child.sendline(":")
child.sendline("=stardict")
child.sendline("!cat examples/test.txt")
child.sendline("<examples/test.txt")
sleep(0.2)
child.sendline("画家")
sleep(0.2)
child.sendline("!")
sleep(0.1)
child.sendline("echo $SHELL")
child.sendline("exit")
child.interact()
