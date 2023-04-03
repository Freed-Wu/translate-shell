# translate-shell

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/translate-shell/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/translate-shell/main)
[![github/workflow](https://github.com/Freed-Wu/translate-shell/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/translate-shell/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/translate-shell/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/translate-shell)
[![readthedocs](https://shields.io/readthedocs/translate-shell)](https://translate-shell.readthedocs.io)
[![DeepSource](https://deepsource.io/gh/Freed-Wu/translate-shell.svg/?show_trend=true)](https://deepsource.io/gh/Freed-Wu/translate-shell)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/translate-shell/total)](https://github.com/Freed-Wu/translate-shell/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/translate-shell/latest/total)](https://github.com/Freed-Wu/translate-shell/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)
[![github/v](https://shields.io/github/v/release/Freed-Wu/translate-shell)](https://github.com/Freed-Wu/translate-shell)

[![pypi/status](https://shields.io/pypi/status/translate-shell)](https://pypi.org/project/translate-shell/#description)
[![pypi/v](https://shields.io/pypi/v/translate-shell)](https://pypi.org/project/translate-shell/#history)
[![pypi/downloads](https://shields.io/pypi/dd/translate-shell)](https://pypi.org/project/translate-shell/#files)
[![pypi/format](https://shields.io/pypi/format/translate-shell)](https://pypi.org/project/translate-shell/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/translate-shell)](https://pypi.org/project/translate-shell/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/translate-shell)](https://pypi.org/project/translate-shell/#files)

Translate text by google, bing, youdaozhiyun, haici, stardict, etc at same time
from CLI, GUI (GNU/Linux, Android, macOS and Windows), REPL, python, shell and vim.

## Usage

### UI

#### CLI

```sh
trans --translators=google,bing,haici,stardict crush
```

![CLI](https://user-images.githubusercontent.com/32936898/205699472-5349d422-54c9-47a3-afc0-53a17f0acaf8.jpg)

#### REPL

```console
$ trans  # enter REPL
> en:ja  # change source language to english and target language to japanese
> :  # swap source and target languages
> =stardict  # use stardict to translate text
> !cat example/test.txt  # execute a shell command
ハッカー
> <example/test.txt   # translate a file
hacker
> 画家  # translate text
painter; artist
> !  # enter shell
$ echo $SHELL  # execute a shell command
/usr/bin/zsh
$ exit  # exit shell
>
```

![REPL](https://user-images.githubusercontent.com/32936898/205617815-3a2ba6b4-2673-4233-907b-202ffd4a9e44.jpg)

#### TUI

##### Vim

```vim
Translate --translators=google,bing Free as in Freedom
```

![Vim](https://user-images.githubusercontent.com/32936898/205475332-61c0a90e-b145-4af0-8658-c0cf45b87150.jpg)

#### GUI

##### GNU/Linux

![GNU/Linux](https://user-images.githubusercontent.com/32936898/205699484-c6fdefd5-dca2-4263-aed4-e41d9d16fde6.jpg)

##### Android

![android-toast](https://user-images.githubusercontent.com/32936898/206078648-0db6480f-7e35-4252-9f33-9fb51e03e172.jpg)

### Script

#### Python

```pycon
>>> from translate_shell.translate import translate
>>> translate("The Mythical Man-Month", "zh_TW")
... Translation(
...     status=1,
...     results=[
...         {
...             "translator": "google",
...             "sl": "auto",
...             "tl": "zh_TW",
...             "text": "The Mythical Man-Month",
...             "phonetic": "",
...             "paraphrase": "人月神話",
...             "explains": {},
...             "details": {},
...             "alternatives": ["神话般的人月"],
...         }
...     ],
...     text="The Mythical Man-Month",
...     to_lang="zh_TW",
...     from_lang="auto",
... )
```

#### Shell Script

```console
$ xsel -o | trans --format json | jq -r '"《\(.results[].paraphrase)》的英文是 \(.text)."'
《大教堂和集市》的英文是 the cathedral and the bazaar.
```

#### Vim Script

```vim
:let g:text = 'Just for Fun'
:let g:translation = json_decode(translate_shell#call('--format=json', g:text))
:echo g:text 'is' g:translation.results[0].paraphrase 'in Chinese.'
Just for Fun is 纯娱乐 in Chinese.
```

## Similar Projects

See [comparison](https://translate-shell.readthedocs.io/en/latest/resources/translator.html).

## Features

- Translate with different translators at same time, like [translator](https://github.com/skywind3000/translator)
- Translate clipboard contents automatically, like [ydcv](https://github.com/felixonmars/ydcv)
- Speak the pronunciation of words
- Support online translate engines
- Support offline dictionaries
- Many methods to use, from shell, python and vim
- Magic text, like `en:` to change source language, `:zh_CN` to change target
  language, `<file` to translate file, etc.
- Allow customization by `config.py`
- Good shell completions, especially for [zsh](https://github.com/zsh-users/zsh),
  complete options and translation history
- Manpage: `man trans`
- Beautiful UI
- Cross platforms
- Rich API, can be easily called from shell and python
- Good document
- Unit test, keep code quality
- CI/CD
- clean code
- Respect [PEP484](https://peps.python.org/pep-0484/)
- Respect [PEP621](https://peps.python.org/pep-0621/)
- Respect [XDG](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

The last but not least: **it is a libre software**.

See [document](https://translate-shell.readthedocs.io) to know more.

PS: PR is welcome! Please make code clean and keep test pass!

<!-- ex: nowrap
-->
