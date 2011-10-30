" wandering color scheme
" Based on the Wandering TextMate theme, by Matthew
" Anderson (http://wanderingmatt.com/), and the ir_black
" vim theme by Todd Werth (http://blog.toddwerth.com/).


" ********************************************************************************
" Standard colors used in all ir_black themes:
" Note, x:x:x are RGB values
"
"  normal: #f6f3e8
" 
"  string: #A8FF60  168:255:96                   
"    string inner (punc, code, etc): #00A0A0  0:160:160
"  number: #FF73FD  255:115:253                 
"  comments: #7C7C7C  124:124:124
"  keywords: #96CBFE  150:203:254             
"  operators: white
"  class: #FFFFB6  255:255:182
"  method declaration name: #FFD2A7  255:210:167
"  regular expression: #E9C062  233:192:98
"    regexp alternate: #FF8000  255:128:0
"    regexp alternate 2: #B18A3D  177:138:61
"  variable: #C6C5FE  198:197:254
"  
" Misc colors:
"  red color (used for whatever): #FF6C60   255:108:96 
"     light red: #FFB6B0   255:182:176
"
"  brown: #E18964  good for special
"
"  lightpurpleish: #FFCCFF
" 
" Interface colors:
"  background color: black
"  cursor (where underscore is used): #FFA560  255:165:96
"  cursor (where block is used): white
"  visual selection: #1D1E2C  
"  current line: #151515  21:21:21
"  search selection: #07281C  7:40:28
"  line number: #3D3D3D  61:61:61


" ********************************************************************************
" The following are the preferred 16 colors for your terminal
"           Colors      Bright Colors
" Black     #4E4E4E     #7C7C7C
" Red       #FF6C60     #FFB6B0
" Green     #A8FF60     #CEFFAB
" Yellow    #FFFFB6     #FFFFCB
" Blue      #96CBFE     #FFFFCB
" Magenta   #FF73FD     #FF9CFE
" Cyan      #C6C5FE     #DFDFFE
" White     #EEEEEE     #FFFFFF


" ********************************************************************************
set background=dark
hi clear

if exists("syntax_on")
  syntax reset
endif

let colors_name = "wandering"


"hi Example         guifg=NONE        guibg=NONE        gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE

" General colors
hi Normal           guifg=#ffffff     guibg=#2c2c2c     gui=NONE      ctermfg=white       ctermbg=black       cterm=NONE
" TOOD: make sure the foreground on the NonText setting makes sense.
hi NonText          guifg=#595f64     guibg=#2c2c2c     gui=NONE      ctermfg=lightgrey      ctermbg=black      cterm=NONE 

hi Cursor           guifg=#2c2c2c     guibg=#5fc344     gui=NONE      ctermfg=black      ctermbg=green      cterm=reverse
hi LineNr           guifg=#3D3D3D     guibg=#2c2c2c     gui=NONE      ctermfg=grey      ctermbg=black      cterm=NONE

hi VertSplit        guifg=#1d1d1d     guibg=#1d1d1d     gui=NONE      ctermfg=grey      ctermbg=grey      cterm=NONE
hi StatusLine       guifg=#4c4c4c     guibg=#1d1d1d     gui=italic    ctermfg=lightgrey      ctermbg=grey      cterm=NONE
hi StatusLineNC     guifg=#2c2c2c     guibg=#1d1d1d     gui=NONE      ctermfg=black      ctermbg=grey      cterm=NONE  

" TODO: Need Folded styling
hi Folded           guifg=#a0a8b0     guibg=#384048     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE
" TODO: Need 'title' styling
hi Title            guifg=#f6f3e8     guibg=NONE        gui=bold      ctermfg=NONE        ctermbg=NONE        cterm=NONE
" TODO: Need 'Visual' styling
hi Visual           guifg=NONE        guibg=#262D51     gui=NONE      ctermfg=NONE        ctermbg=darkgray    cterm=NONE

" TODO: Need 'SpecialKey' styling
hi SpecialKey       guifg=#808080     guibg=#343434     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE

" TODO: Need 'WildMenu' styling
hi WildMenu         guifg=green       guibg=yellow      gui=NONE      ctermfg=black       ctermbg=yellow      cterm=NONE
" TODO: Need 'PmenuSbar' styling
hi PmenuSbar        guifg=black       guibg=white       gui=NONE      ctermfg=black       ctermbg=white       cterm=NONE
"hi Ignore           guifg=gray        guibg=black       gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE

hi Error            guifg=NONE        guibg=NONE        gui=undercurl ctermfg=white       ctermbg=red         cterm=NONE     guisp=#92000e " undercurl color
hi ErrorMsg         guifg=white       guibg=#92000e     gui=BOLD      ctermfg=white       ctermbg=red         cterm=NONE
hi WarningMsg       guifg=white       guibg=#92000e     gui=BOLD      ctermfg=white       ctermbg=red         cterm=NONE

" Message displayed in lower left, such as --INSERT--
hi ModeMsg          guifg=#2c2c2c       guibg=#cfedc6     gui=BOLD      ctermfg=black      ctermbg=cyan        cterm=BOLD

if version >= 700 " Vim 7.x specific colors
  hi CursorLine     guifg=NONE        guibg=#353535     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=BOLD
  hi CursorColumn   guifg=NONE        guibg=#353535     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=BOLD
  hi MatchParen     guifg=#2c2c2c     guibg=#cfedc6     gui=BOLD      ctermfg=black      ctermbg=darkgray    cterm=NONE
  hi Pmenu          guifg=#f6f3e8     guibg=#444444     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE
  hi PmenuSel       guifg=#000000     guibg=#cae682     gui=NONE      ctermfg=NONE        ctermbg=NONE        cterm=NONE
  hi Search         guifg=#2c2c2c     guibg=#e1d896     gui=NONE      ctermfg=black      ctermbg=NONE        cterm=underline
  hi ColorColumn    guifg=NONE        guibg=#353535     gui=NONE      ctermfg=NONE        ctermbg=darkgray    cterm=NONE
endif

" Syntax highlighting
hi Comment          guifg=#6f6f6f     guibg=#424241     gui=NONE      ctermfg=darkgray    ctermbg=NONE        cterm=NONE
hi String           guifg=#75ba53     guibg=NONE        gui=NONE      ctermfg=green       ctermbg=NONE        cterm=NONE
" TODO: Need 'Number' styling -- currently using the 'Constant' rules
hi Number           guifg=#f61500     guibg=NONE        gui=NONE      ctermfg=red         ctermbg=NONE        cterm=NONE

" hi Keyword          guifg=#d3f678     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE
" TODO: Need 'PreProc' styling
hi PreProc          guifg=#96CBFE     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE
hi Conditional      guifg=#d3f678     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE  " if else end

hi Todo             guifg=#cfcfcf     guibg=#424241     gui=NONE      ctermfg=red         ctermbg=NONE        cterm=NONE
hi Constant         guifg=#e9411e     guibg=NONE        gui=NONE      ctermfg=cyan        ctermbg=NONE        cterm=NONE
hi Entity           guifg=#96c8ff     guibg=NONE        gui=NONE      ctermfg=cyan        ctermbg=NONE        cterm=NONE
hi Keyword          guifg=#c8ff65     guibg=NONE        gui=NONE      ctermfg=green       ctermbg=NONE        cterm=NONE

" TODO: These are all using best guesses about what the color should be, based
" on other elements that have been color. Need to refine these styles.
" Using the 'Entity' color
hi Identifier       guifg=#9acafb     guibg=NONE        gui=NONE      ctermfg=cyan        ctermbg=NONE        cterm=NONE
" Using the 'String.regexp.<<special>>' color
hi Function         guifg=#d99043     guibg=NONE        gui=NONE      ctermfg=brown       ctermbg=NONE        cterm=NONE
" Using the 'Type' color
hi Type             guifg=#e1d896     guibg=NONE        gui=NONE      ctermfg=yellow      ctermbg=NONE        cterm=NONE
" Using the 'Support' color
hi Statement        guifg=#c8ff65     guibg=NONE        gui=NONE      ctermfg=lightblue   ctermbg=NONE        cterm=NONE

hi Special          guifg=#ffffff     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
" Using the 'Entity' color
hi Delimiter        guifg=#9acafb     guibg=NONE        gui=NONE      ctermfg=cyan        ctermbg=NONE        cterm=NONE
hi Operator         guifg=#ffffff     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE

hi link Character       Constant
hi link Boolean         Constant
hi link Float           Number
hi link Repeat          Statement
hi link Label           Statement
hi link Exception       Statement
hi link Include         PreProc
hi link Define          PreProc
hi link Macro           PreProc
hi link PreCondit       PreProc
hi link StorageClass    Type
hi link Structure       Type
hi link Typedef         Type
hi link Tag             Special
hi link SpecialChar     Special
hi link SpecialComment  Special
hi link Debug           Special


" Special for Ruby
hi rubyRegexp                  guifg=#e1d896      guibg=NONE      gui=NONE      ctermfg=brown          ctermbg=NONE      cterm=NONE
" TODO: Using the 'String.regexp' style
hi rubyRegexpDelimiter         guifg=#e1d896      guibg=NONE      gui=NONE      ctermfg=brown          ctermbg=NONE      cterm=NONE
hi rubyEscape                  guifg=#ffffff      guibg=NONE      gui=NONE      ctermfg=cyan           ctermbg=NONE      cterm=NONE
" TODO: Using the 'String embedded-source' color
hi rubyInterpolationDelimiter  guifg=#d3f678      guibg=NONE      gui=NONE      ctermfg=blue           ctermbg=NONE      cterm=NONE
" TODO: Using the 'Entity inherited-class'
hi rubyControl                 guifg=#6284a9      guibg=NONE      gui=NONE      ctermfg=blue           ctermbg=NONE      cterm=NONE  "and break, etc
"hi rubyGlobalVariable          guifg=#FFCCFF      guibg=NONE      gui=NONE      ctermfg=lightblue      ctermbg=NONE      cterm=NONE  "yield
hi rubyStringDelimiter         guifg=#a7d562      guibg=NONE      gui=NONE      ctermfg=lightgreen     ctermbg=NONE      cterm=NONE
"rubyInclude
"rubySharpBang
"rubyAccess
"rubyPredefinedVariable
"rubyBoolean
"rubyClassVariable
"rubyBeginEnd
"rubyRepeatModifier
"hi link rubyArrayDelimiter    Special  " [ , , ]
"rubyCurlyBlock  { , , }

hi link rubyClass             Keyword 
hi link rubyModule            Keyword 
hi link rubyKeyword           Keyword 
hi link rubyOperator          Operator
hi link rubyIdentifier        Identifier
hi link rubyInstanceVariable  Identifier
hi link rubyGlobalVariable    Identifier
hi link rubyClassVariable     Identifier
hi link rubyConstant          Type  


" Special for Java
" hi link javaClassDecl    Type
hi link javaScopeDecl         Identifier 
hi link javaCommentTitle      javaDocSeeTag 
hi link javaDocTags           javaDocSeeTag 
hi link javaDocParam          javaDocSeeTag 
hi link javaDocSeeTagParam    javaDocSeeTag 

hi javaDocSeeTag              guifg=#CCCCCC     guibg=NONE        gui=NONE      ctermfg=darkgray    ctermbg=NONE        cterm=NONE
hi javaDocSeeTag              guifg=#CCCCCC     guibg=NONE        gui=NONE      ctermfg=darkgray    ctermbg=NONE        cterm=NONE
"hi javaClassDecl              guifg=#CCFFCC     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE


" Special for XML
hi link xmlTag          Keyword 
hi link xmlTagName      Conditional 
hi link xmlEndTag       Identifier 


" Special for HTML
hi htmlLink                   guifg=#c69ebf     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE

hi link htmlTag         Identifier 
hi link htmlTagName     Identifier 
hi link htmlEndTag      Identifier 


" Special for CSS
hi cssInclude                 guifg=#97a4b6     guibg=NONE        gui=NONE      ctermfg=gray        ctermbg=NONE        cterm=NONE
hi cssBraces                  guifg=#ffffff     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
hi cssTagName                 guifg=#96c8ff     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE
hi cssIdentifier              guifg=#ff5500     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
hi cssClassName               guifg=#ff5500     guibg=NONE        gui=BOLD      ctermfg=white       ctermbg=NONE        cterm=BOLD
hi cssFontAttr                guifg=#198a90     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE
hi cssPseudoClass             guifg=#c69ebf     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
hi cssFunctionName            guifg=#e0db8f     guibg=NONE        gui=NONE      ctermfg=brown       ctermbg=NONE        cterm=NONE
hi cssRenderProp              guifg=#2e98da     guibg=NONE        gui=NONE      ctermfg=blue        ctermbg=NONE        cterm=NONE
hi cssRenderAttr              guifg=#9add51     guibg=NONE        gui=NONE      ctermfg=green       ctermbg=NONE        cterm=NONE
hi cssUrl                     guifg=#5fc344     guibg=NONE        gui=NONE      ctermfg=green      ctermbg=NONE        cterm=NONE
hi cssValueNumber             guifg=#5fc344     guibg=NONE        gui=NONE      ctermfg=green      ctermbg=NONE        cterm=NONE
hi cssUIAttr                  guifg=#5fc344     guibg=NONE        gui=NONE      ctermfg=green      ctermbg=NONE        cterm=NONE

hi link cssPseudoClassId      cssPseudoClass
hi link cssBoxProp            cssRenderProp
hi link cssColorProp          cssRenderProp
hi link cssTextProp           cssRenderProp
hi link cssValueLength        cssRenderAttr
hi link cssTextAttr           cssRenderAttr
hi link cssCommonAttr         cssRenderAttr
hi link cssBoxAttr            cssRenderAttr
hi link cssColor              cssValueNumber
" hi link cssUrl                cssFunctionName


"Special for SCSS
hi scssVariable               guifg=#9caf78     guibg=NONE        gui=BOLD      ctermfg=brown       ctermbg=NONE        cterm=BOLD

hi link scssColor             cssValueNumber
hi link scssAmpersand         scssVariable
hi link scssMixin             cssInclude
hi link scssInclude           cssInclude
hi link scssExtend            cssInclude
hi link scssMixinName         cssFunctionName
hi link scssClass             cssClassName
hi link scssID                cssIdentifier
hi link scssIdChar            scssColor


" Special for Javascript
hi javaScriptType             guifg=#ff9c14     guibg=NONE        gui=NONE      ctermfg=red         ctermbg=NONE        cterm=NONE
hi javaScriptBlock            guifg=#ffffff     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
hi javaScriptParen            guifg=#ffffff     guibg=NONE        gui=NONE      ctermfg=white       ctermbg=NONE        cterm=NONE
hi javaScriptFunction         guifg=#9add51     guibg=NONE        gui=NONE      ctermfg=green       ctermbg=NONE        cterm=NONE
hi javaScriptFuncName         guifg=#96c8ff     guibg=NONE        gui=NONE      ctermfg=cyan        ctermbg=NONE        cterm=NONE
hi javaScriptDocTags          guifg=#dddddd     guibg=#424241     gui=BOLD      ctermfg=gray          ctermbg=NONE        cterm=BOLD
hi javaScriptDocParam         guifg=#c8ff65     guibg=#424241     gui=NONE      ctermfg=cyan

hi link javaScriptFuncBlock   Entity
hi link javaScriptNumber      Number


" Special for Python
"hi  link pythonEscape         Keyword


" Special for CSharp
hi  link csXmlTag             Keyword


" Special for PHP
hi phpIdentifier              guifg=#ff9c14     guibg=NONE        gui=NONE      ctermfg=red         ctermbg=NONE        cterm=NONE
hi phpStorageClass            guifg=#9add51     guibg=NONE        gui=NONE      ctermfg=green       ctermbg=NONE        cterm=NONE

hi link phpOperator           Keyword
hi link phpVarSelector        phpIdentifier
