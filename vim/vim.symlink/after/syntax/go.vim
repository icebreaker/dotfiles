" highlight all types that end with _t (i.e type_t)
syn match Type /\<\i\+_t\>/

" highlight all uppercase "constants"
syn match PreProc /\zs\<[A-Z_][A-Z0-9_]\+\>/

" highlight some common "imports"
syn match Type /\<sdl\..\{-}\>/
syn match Type /\<gl\..\{-}\>/
syn match Type /\<fmt\..\{-}\>/
syn match Type /\<os\..\{-}\>/
syn match Type /\<runtime\..\{-}\>/
syn match Type /\<filepath\..\{-}\>/
syn match Type /\<math\..\{-}\>/

" vim:set sw=2:
