if exists('g:loaded_translate_shell') || &cpoptions
  finish
endif

let s:save_cpoptions = &cpoptions
set cpoptions&vim

""
" Configure if load @plugin(name).
call g:translate_shell#utils#plugin.Flag('g:loaded_translate_shell', 1)

""
" @usage [args]
" Echo the result of calling `trans ...`.
command! -nargs=+ Translate echo translate_shell#call(<f-args>)

let &cpoptions = s:save_cpoptions
unlet s:save_cpoptions
