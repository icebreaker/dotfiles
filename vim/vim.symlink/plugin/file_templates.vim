" Vim global plugin for loading dynamic file skeletons for empty files
"
" Last change:  Mon Jul 24 04:03:59 AEST 2017
" Maintainer:   Damian Conway
" License:      This file is placed in the public domain.
"

if v:version < 800 || exists("g:loaded_file_templates")
    finish
endif
let g:loaded_file_templates = 1

let s:save_cpo = &cpo
set cpo&vim

let s:TEMPLATE_DIR = expand('~/.vim/templates')

augroup FileTemplates
    au!
    au BufNewFile * :call FindAndFillTemplate(expand('<afile>'))
augroup END

function! FindAndFillTemplate(file) abort
	let filepath = fnamemodify(a:file, ':h')
	let filepath = substitute(filepath, '^data/\|^data$\|^src/|^src$/', '', '')
	let filename = fnamemodify(a:file, ':t:r')
	let extension = fnamemodify(a:file, ':e')
	let packagepath = substitute(filepath, '/', '.', 'g')
	let importpath = packagepath . '.'
	if importpath == '.'
		let importpath = ''
	endif

	let variables = {
	\ 'FILENAME'     : filename,
	\ 'EXTENSION'    : extension,
	\ 'FILENAME_PRE' : toupper(filename),
	\ 'EXTENSION_PRE': toupper(extension),
	\ 'FILEPATH'     : filepath,
	\ 'PACKAGEPATH'  : packagepath,
	\ 'IMPORTPATH'   : importpath,
	\ 'YEAR'         : strftime('%Y')
	\}
	let templates = [filename . '.' . extension, extension]

	for template in templates
		let filename = s:TEMPLATE_DIR . '/template.' . template
		if !filereadable(filename)
			continue
		end

		let template = join(readfile(filename), "\n")
		let template = substitute(template, '%\([A-Z_ ]\+\)%', { m -> get(variables, m[1], m[0]) }, 'g')

		call append(0, split(template, "\n"))
		break
	endfor
endfunction

let &cpo = s:save_cpo
