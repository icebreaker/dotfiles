" Location: plugin/asynctotem.vim
" Author:   Mihail Szabolcs <https://mihail.co>
" Version:  1.3
" License:  Same as Vim itself. See :help license

if v:version < 800 || exists('g:asynctotem_loaded')
	finish
endif

let s:save_cpo = &cpo
set cpo&vim

let g:asynctotem_loaded = 1
let g:asynctotem_copen = 0

if !exists('g:asynctotem_copen_keymap')
	let g:asynctotem_copen_keymap = 1
endif

if !exists('g:asynctotem_cclose_delay')
	let g:asynctotem_cclose_delay = 1000
endif

if !exists('g:asynctotem_jump')
	let g:asynctotem_jump = 1
endif

if !exists('g:asynctotem_jump_delay')
	let g:asynctotem_jump_delay = 10
endif

if !exists('g:asynctotem_copen_height')
	let g:asynctotem_copen_height = 0
endif

if !exists('g:asynctotem_cclose_on_kill')
	let g:asynctotem_cclose_on_kill = 0
endif

if !exists('g:asynctotem_cclose_on_no_errors')
	let g:asynctotem_cclose_on_no_errors = 0
endif

if !exists('g:asynctotem_buffer_name')
	let g:asynctotem_buffer_name = 'asynctotem_buffer'
endif

if g:asynctotem_copen_keymap == 1
	augroup asynctotem
		au!
		au BufReadPost quickfix silent exec 'nnoremap q :call asynctotem#cclose()<CR>'
		au BufReadPost quickfix silent exec 'nnoremap <C-c> :call asynctotem#kill()<CR>'
	augroup end
endif

function! asynctotem#copen()
	if g:asynctotem_copen == 1
		return
	else
		let g:asynctotem_copen = 1
	endif

	if g:asynctotem_copen_height > 0
		exec 'copen ' . g:asynctotem_copen_height
	else
		copen
	endif
endfunction

function! asynctotem#jump()
	let n = len(filter(getqflist(), 'v:val.valid'))
	if n == 0
		call asynctotem#cclose()
		wincmd p
		redraw!
		return
	endif

	if g:asynctotem_jump == 0
		redraw!
		return
	endif

	call asynctotem#copen()

	try
		try
			cnext
		catch
			cfirst
		endtry
	catch
		try
			cbottom
		catch
			" noop
		endtry

		call asynctotem#cclose()
		wincmd p
	endtry

	redraw!
endfunction

function! asynctotem#on_cclose(_timer)
	cclose
endfunction

function! asynctotem#on_jump(_timer)
	call asynctotem#jump()
endfunction

function! asynctotem#cclose()
	if g:asynctotem_copen == 0
		return
	else
		let g:asynctotem_copen = 0
	endif

	if !exists('g:asynctotem_job_id')
		if g:asynctotem_cclose_on_kill == 0
			return
		endif
	elseif g:asynctotem_cclose_on_no_errors == 0
		return
	end

	call timer_start(g:asynctotem_cclose_delay, 'asynctotem#on_cclose')
endfunction

function! asynctotem#job_start(cmd)
	call setqflist([])

	if !exists('g:asynctotem_buffer')
		let g:asynctotem_buffer = bufnr(g:asynctotem_buffer_name, 1)
		call setbufvar(g:asynctotem_buffer, '&buftype', 'nofile')
	endif

	let options = {}
	let options.callback = 'asynctotem#on_callback'
	let options.close_cb = 'asynctotem#on_close'
	let options.out_io = 'buffer'
	let options.out_name = g:asynctotem_buffer_name

	let g:asynctotem_cmd = a:cmd
	let g:asynctotem_job_id = job_start(a:cmd, options)
endfunction

function! asynctotem#on_close(_channel)
	if !exists('g:asynctotem_job_id')
		call asynctotem#cclose()
		return
	endif

	call timer_start(g:asynctotem_jump_delay, 'asynctotem#on_jump')
	unlet g:asynctotem_job_id
endfunction

function! asynctotem#on_callback(_channel, message)
	caddexpr a:message
	cbottom
endfunction

function! asynctotem#status()
	if !exists('g:asynctotem_cmd')
		return ''
	endif

	if exists('g:asynctotem_job_id')
		return g:asynctotem_cmd . ' [running]'
	else
		return g:asynctotem_cmd . ' [done]'
	endif
endfunction

function! asynctotem#kill()
	if !exists('g:asynctotem_job_id')
		return
	end

	call job_stop(g:asynctotem_job_id, 'kill')

	unlet g:asynctotem_job_id
endfunction

function! asynctotem#run(...)
	if exists('g:asynctotem_job_id')
		return
	endif

	call asynctotem#copen()
	call asynctotem#job_start(join(a:000))
endfunction

let &cpo = s:save_cpo
" vim:set ts=2 sw=2 sts=2 noet:
