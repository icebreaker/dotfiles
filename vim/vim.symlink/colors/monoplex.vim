"header {{{
" Location:     colors/monoplex.vim
" Author:       Mihail Szabolcs <https://mihail.co>
" Version:      1.0
" License:      Same as Vim itself. See :help license
"}}}
"init {{{
let g:colors_name = 'monoplex'

if has('gui_running') || !exists('syntax_on') || version < 700
	finish
endif

set background=dark

hi clear
syntax reset
"}}}
"general {{{
hi Normal ctermfg=251 ctermbg=0 cterm=NONE
hi NonText ctermfg=251 ctermbg=0 cterm=NONE
hi CursorLine ctermfg=NONE ctermbg=234 cterm=NONE
hi CursorLineNR ctermfg=NONE ctermbg=234 cterm=NONE
hi Cursor ctermfg=NONE ctermbg=NONE cterm=INVERSE
hi LineNr ctermfg=238 ctermbg=NONE cterm=NONE
hi MatchParen ctermfg=255 ctermbg=242 cterm=BOLD
hi Pmenu ctermfg=NONE ctermbg=0 cterm=NONE
hi PmenuSel ctermfg=NONE ctermbg=0 cterm=NONE,INVERSE
hi PmenuSBar ctermfg=NONE ctermbg=0 cterm=NONE
hi PmenuThumb ctermfg=NONE ctermbg=0 cterm=NONE,INVERSE
hi Search ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi IncSearch ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi QuickFixLine ctermfg=NONE ctermbg=NONE cterm=NONE
hi Folded ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi FoldColumn ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi Visual ctermfg=0 ctermbg=251 cterm=NONE
hi StatusLine ctermfg=251 ctermbg=235 cterm=BOLD
hi StatusLineNC ctermfg=251 ctermbg=235 cterm=BOLD,INVERSE
hi StatusLineTerm ctermfg=251 ctermbg=235 cterm=BOLD
hi StatusLineTermNC ctermfg=251 ctermbg=235 cterm=BOLD,INVERSE
hi WildMenu ctermbg=NONE ctermfg=NONE cterm=BOLD,REVERSE
"}}}
"syntax {{{
hi Type ctermfg=172 ctermbg=NONE cterm=BOLD
hi Statement ctermfg=172 ctermbg=NONE cterm=BOLD
hi Function ctermfg=172 ctermbg=NONE cterm=BOLD
hi Identifier ctermfg=172 ctermbg=NONE cterm=BOLD
hi Constant ctermfg=172 ctermbg=NONE cterm=BOLD
hi PreProc ctermfg=172 ctermbg=NONE cterm=BOLD
hi Include ctermfg=172 ctermbg=NONE cterm=BOLD
hi String ctermfg=130 ctermbg=NONE cterm=NONE
hi Special ctermfg=130 ctermbg=NONE cterm=NONE
hi Number ctermfg=130 ctermbg=NONE cterm=NONE
hi Todo ctermfg=172 ctermbg=NONE cterm=BOLD
hi Comment ctermfg=130 ctermbg=NONE cterm=NONE
"}}}
"msg {{{
hi ModeMsg ctermbg=NONE ctermfg=NONE cterm=NONE
hi MoreMsg ctermbg=NONE ctermfg=NONE cterm=NONE
hi WarningMsg ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Ignore ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Question ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Error ctermfg=255 ctermbg=124 cterm=BOLD
hi ErrorMsg ctermfg=255 ctermbg=124 cterm=BOLD
"}}}
"misc {{{
hi Title ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Underlined ctermbg=NONE ctermfg=NONE cterm=UNDERLINE
hi VertSplit ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi Directory ctermfg=NONE ctermbg=NONE cterm=NONE
hi link SpecialKey Special
"}}}
"spell {{{
hi SpellBad ctermfg=255 ctermbg=124 cterm=BOLD
hi! link SpellCap SpellBad
hi! link SpellLocal SpellBad
hi! link SpellRare SpellBad
"}}}
"diff {{{
hi DiffText ctermfg=255 ctermbg=0 cterm=NONE
hi DiffChange ctermfg=255 ctermbg=126 cterm=NONE
hi DiffDelete ctermfg=255 ctermbg=124 cterm=NONE
hi DiffAdd ctermfg=255 ctermbg=23 cterm=NONE
"}}}
"ruby {{{
hi link rubyInstanceVariable Special
hi link rubyGlobalVariable Special
hi link rubyClassVariable Special
"}}}
