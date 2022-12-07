# Install & Uninstall

## [AUR](https://aur.archlinux.org/packages/python-translate-shell)

Install:

```sh
yay -S python-translate-shell
```

uninstall:

```sh
sudo pacman -R python-translate-shell
```

## [PYPI](https://pypi.org/project/translate-shell)

Install:

```sh
pip install translate-shell
```

See [requirements](requirements) to know `extra_requires`.

```sh
pip install 'translate-shell[XXX]'
```

Since now, pip don't support installing man and shell completions.
You must install them manually.

Download shell completions and man from
[releases](https://github.com/Freed-Wu/translate-shell/releases) to correct path:

- bash: `/usr/share/bash-completion/completions/trans`
- zsh: `/usr/share/zsh/site-functions/_trans`
- tcsh: `/etc/profile.d/trans.csh`
- man: `/usr/share/man/man1/trans.1.gz`

**NOTE**: the paths of man and shell completion vary from different OS. The path
of the above code is just for GNU/Linux. For other OSs, do a substitution:

- GNU/Linux, Windows (msys/Msys2, Cygwin): `/usr/share`, `/etc`
- Windows (non-msys/Msys2): `$MINGW_PREFIX/share`,`/etc`
- BSD, Darwin, GNU/Linux (Homebrew): `/usr/local/share`, `/usr/local/etc`
- Android (Termux): `/data/data/com.termux/files/usr/share`,
  `/data/data/com.termux/files/usr/etc`
- Android (Magisk): `/system/usr/share`, `/system/etc`

Uninstall:

```sh
pip uninstall translate-shell
```

Delete shell completions and man by yourself.

## [From Source](https://github.com/Freed-Wu/translate-shell)

Install:

```sh
git clone --depth=1 https://github.com/Freed-Wu/translate-shell
cd translate-shell
make install
```

See [requirements](requirements) to know `extra_requires`.

```sh
make EXTRA='[XXX]' install
```

Uninstall:

```sh
make uninstall
```
