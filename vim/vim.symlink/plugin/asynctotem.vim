" Location:     plugin/asynctotem.vim
" Author:       Mihail Szabolcs <https://mihail.co>
" Version:      1.0
" License:      Same as Vim itself. See :help license

if v:version < 800 || exists('g:asynctotem_loaded') || &cp
  finish
endif

let s:save_cpo = &cpo
set cpo&vim

let g:asynctotem_loaded = 1

if !exists('g:asynctotem_copen_keymap')
  let g:asynctotem_copen_keymap = 1
endif

if !exists('g:asynctotem_cclose_delay')
  let g:asynctotem_cclose_delay = 1000
endif

if !exists('g:asynctotem_cclose_on_kill')
  let g:asynctotem_cclose_on_kill = 0
endif

if !exists('g:asynctotem_cclose_on_no_errors')
  let g:asynctotem_cclose_on_no_errors = 0
endif

function! asynctotem#copen()
  copen

  if g:asynctotem_copen_keymap == 1
    exec 'nnoremap <silent> <buffer> q :cclose<CR>'
	exec 'nnoremap <silent> <buffer> <C-c> :call asynctotem#kill()<CR>'
  endif
endfunction

function! asynctotem#on_cclose(_timer)
  cclose
endfunction

function! asynctotem#cclose()
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
  cexpr []

  let options = {}
  let options.callback = 'asynctotem#on_callback'
  let options.close_cb = 'asynctotem#on_close'
  let options.out_io = 'buffer'
  let options.out_name = 'asynctotem_buffer'

  let g:asynctotem_cmd = a:cmd
  let g:asynctotem_job_id = job_start(a:cmd, options)
endfunction

function! asynctotem#on_close(_channel)
  if !exists('g:asynctotem_job_id')
	call asynctotem#cclose()
	return
  endif

  call asynctotem#copen()

  try
	cnext
  catch
	cbottom
	call asynctotem#cclose()
	wincmd p
  endtry

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
" vim:set sw=2 sts=2:
