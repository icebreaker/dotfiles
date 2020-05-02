" Location:	plugin/gustav.vim
" Author:	Mihail Szabolcs <https://mihail.co>
" Version:	1.0
" License:	Same as Vim itself. See :help license

if exists('g:gustav_loaded') || &cp
  finish
endif

let g:gustav_loaded = 1

if !exists('g:gustav_marked') || !exists('g:gustav_marked_re')
  let g:gustav_marked = '- [x] '
  let g:gustav_marked_re = '^\-\s\[x\]\s'
endif

if !exists('g:gustav_unmarked') || !exists('g:gustav_unmarked_re')
  let g:gustav_unmarked = '- [ ] '
  let g:gustav_unmarked_re = '^\-\s\[\s\]\s'
endif

let s:save_cpo = &cpo
set cpo&vim

function! gustav#add()
  let line = getline('.')

  if len(line) == 0
	call setline('.', g:gustav_unmarked)
  else
    call append('.', g:gustav_unmarked)
	normal! j
  end

  startinsert!
endfunction

function! gustav#toggle()
  let line = getline('.')

  if len(line) == 0
	return
  elseif line =~ g:gustav_unmarked_re
	call setline('.', substitute(line, g:gustav_unmarked_re, g:gustav_marked, ''))
  elseif line =~ g:gustav_marked_re
	call setline('.', substitute(line, g:gustav_marked_re, g:gustav_unmarked, ''))
  endif
endfunction

let &cpo = s:save_cpo
" vim:set sw=2 sts=2:
