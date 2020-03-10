" highlight foreach
syn keyword Function foreach

" highlight all types that end with _t (i.e type_t)
syn match Type /\<\i\+_t\>/

" highlight all uppercase "constants" or "macros"
syn match PreProc /\zs\<[A-Z_][A-Z0-9_]\+\>/

" vim:set sw=2:
