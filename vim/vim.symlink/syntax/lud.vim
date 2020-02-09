if exists('b:current_syntax') && b:current_syntax == 'lud'
  finish
endif

let b:current_syntax = 'lud'

syn keyword luaFunc title subtitle subsubtitle text quote list
syn keyword luaFunc media date code raw table pre config js css
