# Config

The config is the actual feature to make this program is different than other
programs:
I allow user to write config in python, which provide more flexible and free
method to customization. See [file location](resources/man.md#files) to know
where is the config. The file location usually respect standard of every OS
(history file is similar):

- GNU/Linux, Android (Termux), Windows (Msys2, Cygwin):
  `${XDG_CONFIG_HOME:-$HOME/.config}/translate-shell/config.py`
- Windows (native): `%APPDATA%\Local\translate-shell\config.py`
- macOS: `$HOME/Library/translate-shell/config.py`
- dropdown: `$HOME/.translate-shell/config.py`

This is a implementation of <https://github.com/felixonmars/ydcv/issues/55>.

the config file must have a function named `configure()` which input nothing and
return a `Configuration` object. An example is as following:

````python
```{eval-sh}
cd ..
cat examples/config.py
```
````

If you have a completion provided by LSP, you can see which attribute can be
defined:

- [vim](https://github.com/vim/vim) with
  [coc.nvim](https://github.com/neoclide/coc.nvim)
  ![vim](https://user-images.githubusercontent.com/32936898/204821945-9d0b5e56-1a49-433a-9b76-08cf3413e1e3.png)
- [ptpython](https://github.com/prompt-toolkit/ptpython)
  ![ptpython](https://user-images.githubusercontent.com/32936898/205172694-837df6c3-a920-44c0-a2d5-95a021299c58.png)
- [python](https://github.com/python/cpython) with
  [jedi](https://github.com/davidhalter/jedi)
  ![python](https://user-images.githubusercontent.com/32936898/205172684-60f5f910-0dd0-4755-bd0e-05dc1319e9e5.png)

## CLI Options' Default Values

By default,
`trans` is
`trans --source-lang=auto --target-lang=auto --engines=google --format=text --clipboard`.
You can change it in config.
About options' meanings, you can see [options](resources/man.md#options).
About options' legal values, you can see `trans --print-setting`.

```python
# telling translator the source language is faster than let translator detect
config.source_lang = "en"
# target_lang by default is 'auto' which will detect `$LANG`. see `locale`
config.target_lang = "zh_CN"
config.translators = "google,bing,haici"
# Usually you don't need it
config.format = "json"
# Disable translate clipboard automatically
config.clipboard = False
# Translate clipboard every 0.5 seconds
config.sleep_seconds = 0.5
# GUI translation window duration time
config.duration = 20
```

## Logger

By default, python's logging is very ugly:

```pycon
>>> import logging
>>> logging.warning("This is a warning!")
WARNING:root:This is a warning!
```

I advise [rich](https://rich.readthedocs.io/en/latest/logging.html):

```pycon
>>> import logging
>>> from rich.logging import RichHandler
>>> logging.basicConfig(
...     level="INFO",
...     format="%(message)s",
...     handlers=[RichHandler(rich_tracebacks=True, markup=True)],
...     force=True,
... )
>>> logging.warning("This is a warning!")
[11/30/22 07:40:02] WARNING  This is a warning!              <stdin>:1
```

The log has color (different from log level), time, filename and linenumber!
The warning is red and the info is blue. Great!

![color](https://user-images.githubusercontent.com/32936898/204815646-ce28f69a-541e-4b1c-b8f3-0ac6b92a2a62.png)

Default level is `WARNING`, which make `logger.info` will not display. Change it
to `INFO` by `trans --verbose` or `level="INFO"` in `config.py`.

## Secret

Some online translator need user to input a APP ID and secret. However, put
these information in configuration file directly is unsafe. Some user know
`chmod 600`, it is good, however, I can provide a better solution. Let us take
[youdaozhiyun](https://ai.youdao.com) as an example:

Quoted from [ydcv](https://github.com/felixonmars/ydcv)

> ????????????-????????????-???"????????????"??? ????????????-????????????-???????????????API-??????????????????
> ?????????????????????????????????-????????????????????? ??????????????? ID / ??????????????????????????????
> YDAPPID/YDAPPSEC???

[keyring](https://pypi.org/project/keyring) allow to encrypt password, and
[keyring-pass](https://pypi.org/project/keyring-pass) make keyring work with
[pass](https://www.passwordstore.org).

````python
```{eval-sh}
cd ..
cat src/*/utils/youdaozhiyun.py
```
````

Create two secrets `youdaozhiyun/appid` and `youdaozhiyun/appsec` by

```shell
pass insert XXX/XXX
```

When you use youdaozhiyun to translate in the first time, it asks you to input a
[GPG](https://github.com/gpg/gnupg) password to continue, which is more secure.

![gpg](https://user-images.githubusercontent.com/32936898/204803527-bc655fcb-c47d-461a-81a0-d46262844509.png)

This is an implementation of <https://github.com/felixonmars/ydcv/issues/76>.

## Prompt

Default prompt string style is inspired by
[powerlevel10k](https://github.com/romkatv/powerlevel10k). You need install some
requirements to provide [color](resources/requirements.md#color) and
[fonts](https://github.com/ryanoasis/nerd-fonts). All screenshots are using
JetBrainsMono Nerd Font Mono.

You can customize `config.get_prompt`:

```python
from translate_shell.utils.prompt import process_clipboard

def get_prompt(text, tl, sl, translators)
    prompt = sl + ":" + tl + "> "
    return process_clipboard(text, prompt)

config.get_prompt = get_prompt
```

It will give you like

```console
$ trans
auto:zh_CN>
```

The screenshot is same as above in [logger](#logger).

## Process Input

### Magic text

Any user who comes from
[translate-shell (awk)](https://github.com/soimort/translate-shell) know it has
an interesting function, that is user can input `en:zh_CN` to change source
language and target language. I can it `magic text`: any text will be truly
translated. I want to provide user more freedom. By default, we have the
following magic texts:

- `sl:tl` can change source language and target language. `sl:` and `:tl` is same.
- `:` will swap source language and target language.
- `=translator1,translator2,...` will change translators.
- `=` will display current translators.
- `!XXX` will execute `XXX` in shell command.
- `!` will execute `$SHELL` or `sh` if `$SHELL` is not exist.
- `<filename` will translate file contents.

Some magic texts are inspired by shell.

### Preprocess

And we will preprocess the non-magic text:

- convert `\t` to ' ', useful for translate programming variables
- strip trailing whitespaces, reduce length due to limitation of some
  translation engines
- strip redundant whitespaces, reduce length due to limitation of some
  translation engines
- remove `-\n`, useful for reading pdf
- convert `\n` to ' ', useful for reading pdf
- change `get_char` to `get char`, useful for translate programming variables
- change `getChar` to `get char`, useful for translate programming variables
- lowercase, useful for translate programming variables

Refer <https://github.com/felixonmars/ydcv/issues/67>:

![paper](https://user-images.githubusercontent.com/32936898/180610184-008b7eb8-c20e-494e-a391-efe0844b0fca.png)

The clipboard get

> Some earlier results suggest\\n
> that incorporating local normalization in linear block transform coding
> methods can improve cod-\\n
> ing performance

If we don't preprocess text, the result of youdaozhiyun will be:

> ???????????????????????????\\n
> ?????????????????????????????????????????????????????????????????????????????????\\n
> ??????????????????(ing)??????

It is not your need, I believe.

After preprocess:

> Some earlier results suggest that incorporating local normalization in linear
> block transform coding methods can improve coding performance

The result is your need:

> ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????

This [PR](https://github.com/felixonmars/ydcv/issues/67) has been ignored by
the author, so I have to create this software for myself.

You can customize `config.process_input`.

## Process output

You can customize `config.process_output`. Same as [prompt](#prompt), a p10k
output style has been provided.

You can customize `config.process_output`:

```python
def process_output(translation):
    text = "\n".join(
        "\n".join(
            [rst["translator"] + ":", rst["paraphrase"] + rst["phonetic"]]
            + [k + " " + v for k, v in rst["explains"].items()]
        )
        for rst in translation.results
    )
    return text


config.process_output = process_output
```

The screenshot is same as above in [logger](#logger).

## Translate Clipboard

In REPL, translate-shell can translate any content in clipboard, when it has
changed.

You can customize `config.get_clipper`.

## Speaker

See [speaker](resources/translator.md#speaker)

You can customize `config.get_speaker`.

## Readline Complete

See [readline](resources/readline.md#readline)

You can customize `config.complete`.
