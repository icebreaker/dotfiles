au BufRead,BufNewFile *.zig set filetype=zig
au BufRead,BufNewFile *.zir set filetype=zir
au Filetype zig setlocal makeprg=zig\ build\ --prefix\ build\ $*
