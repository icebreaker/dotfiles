" Location: plugin/fastopen.vim
" Author:   Mihail Szabolcs <https://mihail.co>
" Version:  1.6
" License:  Same as Vim itself. See :help license

if exists('g:loaded_fastopen') || &cp
	finish
endif

let g:loaded_fastopen = 1

if !exists('g:fastopen_dmenu_cmd')
	let g:fastopen_dmenu_cmd = 'dmenu -i -l 10'
endif

if !exists('g:fastopen_list_fallback_cmd')
	let g:fastopen_list_fallback_cmd = 'find . -type f'
endif

if !exists('g:fastopen_list_cmd')
	let g:fastopen_list_cmd = g:fastopen_list_fallback_cmd
else
	let s:initialized = 1
endif

if !exists('g:fastopen_dir')
	let g:fastopen_dir = ''
else
	let s:initialized = 1
endif

function! s:find_git_dir()
	if exists('b:git_dir')
		return b:git_dir
	endif

	return FugitiveGitDir()
endfunction

function! s:initialize()
	if exists('s:initialized')
		return
	endif

	if !exists('g:loaded_fugitive')
		let s:initialized = 1
		return
	endif

	if exists('g:fastopen_git_aware')
		let g:fastopen_list_cmd = g:fastopen_list_fallback_cmd
		let g:fastopen_dir = ''
	else
		let s:initialized = 1
	end

	let git_dir = s:find_git_dir()
	if empty(git_dir)
		return
	endif

	let open_dir = substitute(git_dir, '\.git$', '', '')
	if empty(open_dir)
		return
	endif

	let g:fastopen_list_cmd = 'git -C ' . shellescape(open_dir)  .  ' ls-files -c -o --full-name --exclude-standard'
	let g:fastopen_dir = open_dir
endfunction

function! fastopen#show(cmd)
	call s:initialize()

	let cmd = g:fastopen_list_cmd

	if cmd =~ '^find ' && fnamemodify('~', ':p') =~ getcwd()
		let cmd .= ' -maxdepth 1'
	endif

	if exists('g:fastopen_filter_cmd')
		let cmd .= ' | ' . g:fastopen_filter_cmd
	endif

	let file = system(cmd . ' | ' . g:fastopen_dmenu_cmd)
	if v:shell_error != 0
		echohl ErrorMsg
		echon file
		echohl None
		return
	endif

	let file = substitute(file, '\n$', '', '')

	if empty(file)
		return
	endif

	execute a:cmd . ' ' . fnameescape(g:fastopen_dir . file)
endfunction

" vim:set ts=2 sw=2 sts=2 noet:
