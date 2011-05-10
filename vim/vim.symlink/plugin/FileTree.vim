" FileTree - treeview file explorer for vim
"
" Author:  Yury Altukhou
" Date:    2004-11-24
" Email:   wind-xp@tut.by
" Version: 1.0
"
" see :help FileTree.txt for detailed description


let FileTree_VERSION='1.0'

try  
	runtim plugin/tree.vim
	if Tree_VERSION<'1.0'
		throw 'E484'
	endif
catch /E121.*/
	throw "FileTree_Error: You have to have tree.vim srcipt at least 1.0" 
endtry 

" setup command 

command! -nargs=* -complete=dir FileTree call FileTree(FileTree_Orientation,FileTree_Side,<f-args>)
command! -nargs=* -complete=dir LFileTree call FileTree(Tree_VerticalSplit,Tree_Left,<f-args>)
command! -nargs=* -complete=dir RFileTree call FileTree(Tree_VerticalSplit,Tree_Right,<f-args>)
command! -nargs=* -complete=dir TFileTree call FileTree(Tree_HorizontalSplit,Tree_Top,<f-args>)
command! -nargs=* -complete=dir BFileTree call FileTree(Tree_HorizontalSplit,Tree_Below,<f-args>)
command! -nargs=* -complete=dir CD call FileTree_CD(<f-args>)
command! -nargs=0 Popd call FileTree_Popd()
command! -nargs=1 -complete=dir Pushd call FileTree_Pushd(<f-args>)
command! -nargs=0 Dirs echo FileTree_Dirs()



" used variables 
"
" b:file_match_pattern  - filtering pattern
" b:show_hidden_files -- whether to show hidden files ( thous whith '.')
" b:FILETREE_BUFFER -- says that it is FileTree Buffer
" s:ATTRIBUTE_SEPARATOR=':'
" b:FileTree_directoryStack - string[] - a list of directories

let g:FileTree_title = "[FileTree]"

function! FileTree_Start()
  call FileTree(0,0)
endfunction

function! FileTree_IsValid()
  return 1
endfunction

 function! FileTree(orientation,side,...) 
	" create explorer window
	" take argument as path, if given
 	if a:0>0 
		let path=a:1
	else
		" otherwise current dir
		let path=getcwd()
	end 

	let path=s:NormalizePath(path)
	"remove all trailing '/' or '\'
	let path=s:RemoveTrailingSlashes(path)
	call Tree_NewTreeWindow (path.'<d>',a:orientation,a:side,g:FileTree_WindowWidth,g:FileTree_WindowHeigh,"FileTree_InitOptions")
endfunction 

function! FileTree_CD (...) 
	if !exists("b:FILETREE_BUFFER") 
		"if this is not File tree buffer
		return
	endif 
	if a:0==0 
		"on empty path go $HOME
		let path="~"
	else
		let path=a:1
	endif 
	if path=='-' 
		"go to previous directory
		lcd -
		let path =getcwd()
		lcd -
		return FileTree_CD (path)
	end 
	if path[0]=='=' 
		"if path is =n then go to nth directory in the stack
		let path=strpart(path,1)
		let path=FileTree_GetDirecoryInTheStack(path)
	end 
	let path=s:NormalizePath(path)
	let path=s:RemoveTrailingSlashes(path)
	call Tree_SetPath(path)
endfunction 

function! FileTree_Pushd(path) 
	if !exists("b:FILETREE_BUFFER") 
		"if this is not File tree buffer
		return
	endif 
	let path=s:NormalizePath(a:path)
	let b:FileTree_directoryStack=path."\n".b:FileTree_directoryStack
endfunction 

function! FileTree_Popd() 
	if !exists("b:FILETREE_BUFFER") 
		"if this is not File tree buffer
		return
	endif 
	if b:FileTree_directoryStack=='' 
		throw "FileTree_Error: direcotry stack is empty"
	endif 
	let path=GetNextLine(b:FileTree_directoryStack)
	let b:FileTree_directoryStack=CutFirstLine(b:FileTree_directoryStack)
	call FileTree_CD (path)
endfunction 

function! FileTree_Dirs() 
	if !exists("b:FILETREE_BUFFER") 
		"if this is not File tree buffer
		return
	endif 
	let stack=b:FileTree_directoryStack
	let newStack=''
	let i=0
	while stack!='' 
		let entry=GetNextLine(stack)
		let entry=i."\t".entry
		let newStack=newStack."\n".entry
		let i=i+1
		let stack=CutFirstLine(stack)
	endwhile 
	return newStack 
endfunction 

function! FileTree_GetDirecoryInTheStack(aNumber) 
	if !exists("b:FILETREE_BUFFER") 
		"if this is not File tree buffer
		return
	endif 
	let stack=b:FileTree_directoryStack
	let i=a:aNumber
	while i>0  
		let stack=CutFirstLine(stack)
		let i=i-1
	endwhile 
	return GetNextLine(stack)
endfunction 

" callback functions for Tree Plugin

function! FileTree_InitOptions () 
	let b:FileTree_directoryStack=''
	let b:FILETREE_BUFFER=1
	let b:Tree_pathSeparator=s:FileTree_pathSeparator
	let s:ATTRIBUTE_SEPARATOR=':'
	let b:Tree_ColorFunction="FileTree_InitColors" 
	let b:Tree_IsLeafFunction="FileTree_IsLeaf" 
	let b:Tree_GetSubNodesFunction="FileTree_GetSubNodes" 
	let b:Tree_InitMappingsFunction="FileTree_InitMappings" 
	let b:Tree_OnLeafClick="FileTree_OnLeafClick"
	let b:Tree_OnPathChange="FileTree_OnPathChange"
	let b:file_match_pattern="*"
	let b:show_hidden_files=0
endfunction 

function! FileTree_InitColors ()  

	syn match Directory  "[^<>]\+\ze<d.*>"
	syn match File "[^<>]\+\ze<f.*>"
	syn match VimFile "[^<>]\+\.vim\ze<f.*>"
	syn match Hidden "<[^<>]*>"

	hi link FIle Label
	hi link VimFIle Label
	hi link Hidden Ignore	
	hi link Directory  Comment
endfunction 

function! FileTree_InitMappings () 
	noremap <silent> <buffer> M :call <SID>SetMatchPattern ()<CR>
	noremap <silent> <buffer> H :call <SID>ToggleShowHidden ()<CR>
	noremap <silent> <buffer> T :call <SID>FileCreate ()<CR>
	noremap <silent> <buffer> S :call <SID>FileSee ()<CR>
	noremap <silent> <buffer> N :call <SID>FileRename ()<CR>
	noremap <silent> <buffer> D :call <SID>FileDelete ()<CR>
	noremap <silent> <buffer> C :call <SID>FileCopy ()<CR>
	noremap <silent> <buffer> O :call <SID>FileMove ()<CR>
  noremap <silent> <buffer> R :call <SID>RefreshTree ()<CR>
  noremap <silent> <buffer> U :call <SID>UpTree ()<CR>
endfunction	

function! FileTree_IsLeaf (path)  
	let attributes=s:GetAttributes(a:path)
	return attributes[0]=='f' 
endfunction 

function! FileTree_GetSubNodes (path)  
	return s:ListDirEntries(a:path)
endfunction 

function! FileTree_OnLeafClick (path) 
	let path =s:RemoveAttributes(a:path)
	call s:OpenFile (path)
endfunction 

function! FileTree_OnPathChange( path) 
	let path=substitute(a:path,' ','\\ ','g')
	let path=s:RemoveAttributes(path)
	execute "lcd ".path.s:FileTree_pathSeparator
endfunction 

" script private functions
function s:RefreshTree()
  call FileTree_CD('.')
endfunction

function s:UpTree()
  call FileTree_CD('..')
endfunction

 function! s:NormalizePath(path) 
	let path=fnamemodify(expand(a:path.s:FileTree_pathSeparator),":p")
	"let path=fnamemodify(expand(a:path.s:FileTree_pathSeparator),":~")
	return path
endfunction 

function! s:Init () 
	if has('win32') || has('dos32') || has('win16') || has('dos16') || has('win95') 
		let s:FileTree_pathSeparator='\'
	else
		let s:FileTree_pathSeparator='/'
	end 
	if !exists("g:FileTree_WindowHeigh") 
		let g:FileTree_WindowHeigh=10
	endif 
	if !exists("g:FileTree_WindowWidth") 
		let g:FileTree_WindowWidth=21
	endif 
	if !exists("g:FileTree_Orientation") 
		let g:FileTree_Orientation=1
	endif 
	if !exists("FileTree_Side") 
		let g:FileTree_Side=0
	endif 
endfunction 

function! s:OpenFile (path) 
	if filereadable(a:path) 
		" go to last accessed buffer
		"wincmd p
		" append sequence for opening file
    "execute "cd ".fnamemodify(a:path,":h")
    "execute "e ".a:path
		"setlocal modifiable
    call WinManagerFileEdit(a:path,0)
	endif 
endfunction 

function! s:ListDirEntries(path) 
	let path=<SID>RemoveAttributes(a:path).b:Tree_pathSeparator
	let attributes=s:GetAttributes(a:path)
	"find all files in the directory
	let fileList=glob(path.b:file_match_pattern)."\n"
	if b:show_hidden_files 
		" find all hidden files 
		let fileList=fileList.glob(path.'.'.b:file_match_pattern)."\n"
	endif 

	let fls=''
	let dirs="\n"

	let path=escape(path,"\\")

	while strlen(fileList)>0 
		let entry=GetNextLine (fileList)
		let fileList=CutFirstLine(fileList)

		"skipping empty entries
		if entry==''  
			continue
		endif 

		if isdirectory(entry)  
			"if entry is directory then mark it with d flag
			let entry=s:RemoveTrailingSlashes(entry)
			let entry=entry."<d>"
			let entry=substitute (entry,path,'','g')
			let dirs=dirs.entry."\n"
		else
			"if entry is file then mark it with f flag
			let entry=entry."<f>"
			let entry=substitute (entry,path,'','g')
			let fls=fls.entry."\n"
		endif 
	endwhile 

	"remove . && .. directories
	"let dirs=substitute(dirs,"\n..<d>\n",'\n','g')
	"let dirs=substitute(dirs,"\n.<d>\n",'\n','g')
	return dirs.fls
endfunction 

function! s:IsDirectory(path) 
	let path=s:RemoveAttributes (a:path)
	let attributes=s:GetAttributes (a:path)
	return attributes[0]!='f'
endfunction 

function! s:SetMatchPattern () 
	let b:file_match_pattern=input ("Match pattern: ",b:file_match_pattern)
	call Tree_RebuildTree()
endfunction 

function! s:ToggleShowHidden() 
	let b:show_hidden_files = 1-b:show_hidden_files
	call Tree_RebuildTree()
endfunction 

function! s:GetPathUnderCursor () 
	let path=Tree_GetPathUnderCursor()
	return <SID>RemoveAttributes (path)
endfunction 

function! s:RemoveAttributes (path) 
	return substitute(a:path,"<[^><]*>",'','g')
endfunction 

function! s:GetAttributes (path) 
	return substitute(a:path,'.*<\([^<>]*\)>$','\1','')
endfunction 

function! s:InsertFilename() 
	"normal 1|g^
	let filename=<SID>GetPathUnderCursor()
	wincmd p
	execute "normal a".filename
endfunction 

function! s:InsertFileContent() 
	"norm 1|g^
	let filename=<SID>GetPathUnderCursor()
	if filereadable(filename) 
		wincmd p
		execute "r ".filename
	endif 
endfunction 

function! s:FileCreate()
	let dirname=<SID>GetPathUnderCursor()
  if isdirectory(dirname)
		let newfilename=input("New file: ",dirname."/")
    "if newfilename
      let i=system("touch ".newfilename)
      call Tree_RebuildTree ()	
    "end
  endif
endfunction


function! s:FileSee() 
	let filename=<SID>GetPathUnderCursor()
	if filereadable(filename) 
		let i=system("open ".filename."&")
	endif 
endf 

function! s:FileRename() 
	let filename=<SID>GetPathUnderCursor()
	if filereadable(filename) 
		let newfilename=input("Rename to: ",filename)
		if filereadable(newfilename) 
			if input("File exists, overwrite?")=~"^[yY]" 
				setlocal ma
				let i=rename(filename,newfilename)
				" refresh display
				normal gg$
				call Tree_RebuildTree ()
			endif 
		else
			" rename file
			setlocal ma
			let i=rename(filename,newfilename)
			normal gg$
			call Tree_RebuildTree ()

		endif 
	endif 
endf 

function! s:FileDelete() 
	let filename=<SID>GetPathUnderCursor()
	if filereadable(filename) 
		if input("OK to delete ".fnamemodify(filename,":t")."? ")[0]=~"[yY]" 
			let i=delete(filename)
			setlocal modifiable
			normal ddg^
			setlocal nomodifiable nomodified
		endif 
	endif  
endfunction 

function! s:FileCopy() 
	let filename=<SID>GetPathUnderCursor()
	if filereadable(filename) 
		let newfilename=input("Copy to: ",filename)
		if filereadable(newfilename) 
			if input("File exists, overwrite?")=~"^[yY]" 
				" copy file
				let i=system("cp -f ".filename." ".newfilename)
				call Tree_RebuildTree()	
			endif 
		else
			" copy file
			let i=system("cp ".filename." ".newfilename)
			call Tree_RebuildTree()
		endif 
	endif 
endfunction 

function! s:FileMove() 
	let filename=<SID>GetPathUnderCursor ()
	if filereadable(filename) 
		let newfilename=input("Move to: ",filename)
		if filereadable(newfilename) 
			if input("File exists, overwrite?")=~"^[yY]" 
				" move file
				let i=rename(filename,newfilename)
				call Tree_RebuildTree()
			endif 
		else
			" move file
			let i=rename(filename,newfilename)
			call Tree_RebuildTree()
		endif 
	endif 
endfunction  

function! s:RemoveTrailingSlashes(path) 
		let path=substitute(a:path,'\'.s:FileTree_pathSeparator."*$",'','')
		if path=='' 
			let path='/'
		endif
		return path
endfunction 

call s:Init()
