# Readline

This program uses readline which is installed by default in linux and macOS (in
fact, macOS uses a compatible editline). About configuration of readline, you
can see
<https://www.gnu.org/software/bash/manual/html_node/Readline-Init-File-Syntax.html>
or refer [my dotfile](https://github.com/Freed-Wu/my-dotfiles/blob/main/.inputrc).

A suggested program is
[fzf-tab-completion](https://github.com/lincheney/fzf-tab-completion) which
allow you to use fzf to complete readline.

I realize a tab complete function to let user use readline better:

```console
$ trans
> <TAB>
! : < = en zh_CN ...
> !<TAB>
!ls   !cp   !rm   ...
> <<TAB>
<file1        <dir1/
> <dir1/<TAB>
<dir1/file1   <dir1/file2
> :<TAB>
: :en :zh_CN ...
> en:<TAB>
en: en:en en:zh_CN ...
> =<TAB>
=bing   =google   =stardict   ...
> =bing<TAB>
=bing,
> =bing,<TAB>
=bing,google    =bing,stardict    ...
```

You can customize it if you like.

## Hotkeys

See <https://www.gnu.org/software/bash/manual/html_node/Readline-Interaction.html>.

Especially, `<M-BS>` can be more useful than `<C-W>`:

```console
$ trans
> <dir1/dir2/file1<M-BS>
<dir1/dir2/
> <dir1/dir2/file1<C-W>

> =bing,google<M-BS>
=bing,
> =bing,google<C-W>

```
