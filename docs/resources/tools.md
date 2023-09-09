# Tools

## `python -m translate_shell.tools.po`

A command line interface of
[github action](https://translate-shell.readthedocs.io/en/latest/#github-action).

## `python -m translate_shell.tools.generate_prompt`

A tool to generate a prompt for:

### [lftp](https://github.com/lavv17/lftp/discussions/711)

```sh
install -d ~/.config/lftp/lftp
python -m translate_shell.tools.generate_prompt > ~/.config/lftp/lftp/rc
echo 'source ~/.config/lftp/lftp/rc' >> ~/.config/lftp/rc
```

![lftp](https://github.com/lavv17/lftp/assets/32936898/e2193cda-2ac0-4020-ac3b-a7ac2156cff6)

### [gdb](https://github.com/Freed-Wu/gdb-prompt#alternatives)

```sh
touch ~/.config/gdb/gdbinit
install -d ~/.config/gdb/gdb
python -m translate_shell.tools.generate_prompt \
    --format='set extended-prompt {text}' \
    --prompt-string="\n(gdb) " \
    --section WHITE BLUE ' \w' \
    --section WHITE BLACK '󰊕 \f' \
    --section BLACK YELLOW ' \t ' >> ~/.config/gdb/gdb/gdbinit
echo 'source ~/.config/gdb/gdb/gdbinit' >> ~/.config/gdb/gdbinit
```

![gdb](https://user-images.githubusercontent.com/32936898/263782466-4dd002fd-9259-4d44-a854-5e132c32b4db.png)

## `python -m translate_shell.tools.repl`

Enter a beautiful REPL for python. Or add the following code to your
[`$PYTHONSTARTUP`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSTARTUP):

```python
from translate_shell.tools.repl.main import interact

interact()
```

![python](https://user-images.githubusercontent.com/32936898/205494856-6f11d1a1-b2e3-469d-91c7-8a24c400fa78.jpg)
