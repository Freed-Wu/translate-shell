# Configure for Language Servers

## (Neo)[Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

```json
{
  "languageserver": {
    "translate": {
      "command": "trans",
      "args": [
        "--lsp"
      ],
      "filetypes": [
        "text"
      ]
    }
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

```vim
if executable('trans')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'translate',
          \ 'cmd': {server_info->['trans', '--lsp']},
          \ 'whitelist': ['text'],
          \ })
  augroup END
endif
```

## [Neovim](https://neovim.io)

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "*.txt" },
  callback = function()
    vim.lsp.start({
      name = "translate",
      cmd = { "trans" "--lsp" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "trans" "--lsp")))
  :activation-fn (lsp-activate-on "*.txt")
  :server-id "translate")))
```

## [Sublime](https://www.sublimetext.com)

```json
{
  "clients": {
    "translate": {
      "command": [
        "trans",
        "--lsp"
      ],
      "enabled": true,
      "selector": "source.text"
    }
  }
}
```
