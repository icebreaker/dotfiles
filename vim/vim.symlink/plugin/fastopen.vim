" Location:     plugin/fastopen.vim
" Author:       Mihail Szabolcs <http://mihail.co>
" Version:      1.1
" License:      Same as Vim itself.  See :help license

if exists('g:loaded_fastopen') || &cp
  finish
endif

let g:loaded_fastopen = 1

if !exists('g:fastopen_dmenu_cmd')
  let g:fastopen_dmenu_cmd = 'dmenu -i -l 10'
endif

if !exists('g:fastopen_list_cmd')
  let g:fastopen_list_cmd = 'find . -type f'
else
  let s:initialized = 1
endif

if !exists('g:fastopen_dir')
  let g:fastopen_dir = ''
else
  let s:initialized = 1
endif

function! s:initialize()
  if exists('s:initialized')
	return
  endif

  let s:initialized = 1

  if !exists('g:loaded_fugitive')
	return
  endif

  let git_dir = substitute(fugitive#extract_git_dir(expand('%:p')), '\.git$', '', '')
  
  if empty(git_dir)
	return
  endif

  let git_cmd = 'git ls-files -c -m -o --full-name --exclude-standard'

  let g:fastopen_list_cmd = git_cmd . ' ' . git_dir
  let g:fastopen_dir = git_dir
endfunction

function! fastopen#show(cmd)
	call s:initialize()

	let cmd = g:fastopen_list_cmd

	if exists('g:fastopen_filter_cmd')
	  let cmd .= ' | ' . g:fastopen_filter_cmd
	endif

	let file = system(cmd . ' | ' . g:fastopen_dmenu_cmd)
	let file = substitute(file, '\n$', '', '')
	
	if empty(file)
		return
	endif

	execute a:cmd . ' ' . g:fastopen_dir . file
endfunction

" vim:set sw=2 sts=2:
