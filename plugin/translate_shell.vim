if exists('g:loaded_translate_shell') || &cpoptions
  finish
endif

let s:save_cpoptions = &cpoptions
set cpoptions&vim

""
" configure if load @plugin(name)
call g:translate_shell#utils#plugin.Flag('g:loaded_translate_shell', 1)

command! -nargs=+ Translate call translate_shell#echo(<f-args>)

let &cpoptions = s:save_cpoptions
unlet s:save_cpoptions
