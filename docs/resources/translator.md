# Translator

A translator is a function which input text, target language and source
language then do something according to inputs and output a result.

Current translators are:

```{eval-sh}
cd ..
scripts/generate-translator.md.py
```

Some translators are out of box and some need configuration, which detail can be
found by clicking the above hyperlink.

**NOTE**:

- stardict and haici only support translate word, not sentence.
- bing supports swapping languages automatically, which means `en:zh_CN` is
  same as `zh_CN:en`.
- haici is the slowest translator currently which often timeout.

These translators can be divided to three types:

## Speaker

Speaker play the pronunciation of text in target language. Now it only use
offline software to speak. See `trans --print-setting speaker`.

- <https://github.com/voldikss/vim-translator/issues/68> Online speaker is a
  little hard to realize.
- <https://github.com/felixonmars/ydcv/blob/2db05d41e1fc927cd0c49aad101ed6a21ad92c2b/src/ydcv.py#L148-L158>
  speaks by youdaozhiyun.

## Offline Translators

Now only support [stardict](translate_shell.translators.stardict).
Offline translator requires user to download
[dictionary](http://download.huzheng.org) in advance.
If you have a package manager, you can use it to download, too:

```shell
yay -S stardict-langdao-ec-gb stardict-langdao-ce-gb stardict-jmdict-ja-en stardict-jmdict-en-ja
```

- [stardict](https://github.com/huzheng001/stardict-3) the famous dictionary.
- [stardict](https://github.com/Dushistov/sdcv) a console version of
  [stardict](https://github.com/huzheng001/stardict-3).
- [ecdict](https://github.com/skywind3000/ECDICT) a collection of high frequency
  vocabulary.
- [coc-ecdict](https://github.com/fannheyward/coc-ecdict) a port of
  [ecdict](https://github.com/skywind3000/ECDICT) for
  [coc.nvim](https://github.com/neoclide/coc.nvim).

## Online Translators

Offline translator translate text by online translate engines.

- [translate-shell (awk)](https://github.com/soimort/translate-shell):
  written in [gawk](https://github.com/onetrueawk/awk).
  I am in respect to a developer can use gawk to write a good software.
  However, I cannot do any help because I don't know awk.
  It has a inspiring feature which user can use magic text like `en:zh_CN` to
  change some settings when in REPL.
  I realize it and use its name to name this program to salute.
- [translator](https://github.com/skywind3000/translator) should be the first
  CLI program to translate text by many different online translate engines at
  once to the best of my knowledge. I use multi threads to realize it.
- [vim-translator](https://github.com/voldikss/vim-translator) a port of
  [translator](https://github.com/skywind3000/translator) for
  [vim](https://github.com/vim/vim) which has a good support for vim.
- [coc-translator](https://github.com/voldikss/coc-translator) a rewrite of
  [translator](https://github.com/skywind3000/translator) for
  [coc.nvim](https://github.com/neoclide/coc.nvim), which has a good support for
  vim. :+1:
- [ydcv](https://github.com/felixonmars/ydcv) only support youdaozhiyun.
- [wudao-dict](https://github.com/ChestnutHeng/Wudao-dict) only support youdao.
- [deepl](https://github.com/DeepLcom/deepl-python) It is said it's the most
  accurate translate engine.
- [crow-translate](https://github.com/crow-translate) has both GUI and CLI
  interface and supports OCR. :+1:
