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
hi WildMenu ctermbg=NONE ctermfg=NONE cterm=BOLD,REVERSE
"}}}
"syntax {{{
hi Type ctermfg=172 ctermbg=NONE cterm=BOLD
hi Statement ctermfg=134 ctermbg=NONE cterm=BOLD
hi Function ctermfg=68 ctermbg=NONE cterm=BOLD
hi Identifier ctermfg=132 ctermbg=NONE cterm=BOLD
hi Constant ctermfg=185 ctermbg=NONE cterm=BOLD
hi PreProc ctermfg=31 ctermbg=NONE cterm=BOLD
hi Include ctermfg=131 ctermbg=NONE cterm=BOLD
hi String ctermfg=137 ctermbg=NONE cterm=NONE
hi Special ctermfg=29 ctermbg=NONE cterm=NONE
hi Number ctermfg=130 ctermbg=NONE cterm=NONE
hi Todo ctermfg=243 ctermbg=NONE cterm=BOLD
hi Comment ctermfg=238 ctermbg=NONE cterm=NONE
"}}}
"msg {{{
hi ModeMsg ctermbg=NONE ctermfg=NONE cterm=NONE
hi MoreMsg ctermbg=NONE ctermfg=NONE cterm=NONE
hi WarningMsg ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Ignore ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Question ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Error ctermfg=NONE ctermbg=124 cterm=BOLD
hi ErrorMsg ctermfg=NONE ctermbg=124 cterm=BOLD
"}}}
"misc {{{
hi Title ctermfg=NONE ctermbg=NONE cterm=BOLD
hi Underlined ctermbg=NONE ctermfg=NONE cterm=UNDERLINE
hi VertSplit ctermfg=NONE ctermbg=NONE cterm=BOLD,INVERSE
hi Directory ctermfg=NONE ctermbg=NONE cterm=NONE
hi link SpecialKey Special
"}}}
"spell {{{
hi SpellBad ctermfg=124 ctermbg=NONE cterm=BOLD
hi! link SpellCap SpellBad
hi! link SpellLocal SpellBad
hi! link SpellRare SpellBad
"}}}
"diff {{{
hi DiffText ctermfg=NONE ctermbg=NONE cterm=NONE
hi DiffChange ctermfg=NONE ctermbg=29 cterm=NONE
hi DiffDelete ctermfg=NONE ctermbg=125 cterm=NONE
hi DiffAdd ctermfg=NONE ctermbg=28 cterm=NONE
"}}}
"ruby {{{
hi link rubyInstanceVariable Special
hi link rubyGlobalVariable Special
hi link rubyClassVariable Special
"}}}
