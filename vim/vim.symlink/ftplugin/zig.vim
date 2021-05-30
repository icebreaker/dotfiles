if exists('b:did_ftplugin')
  finish
endif
let b:did_ftplugin = 1

" match zig built-in fns
setlocal iskeyword+=@-@

" ensure that we expand spaces to tabs
setlocal expandtab
setlocal tabstop=4
setlocal shiftwidth=4
setlocal softtabstop=4

" allow :make and :make run, etc
setlocal makeprg=zig\ build\ --prefix\ build\ $*

" prepend correct 'zig cc' friendly error format
let &l:errorformat .= 'error(compilation):\ clang\ failed\ with\ stderr:\ %f:%l:%c:\ %m'
