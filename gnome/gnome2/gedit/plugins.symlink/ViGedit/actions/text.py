########################
###
###   DELETION
###
########################

def delete_Selection(act):
    act.bindings.mode = act.modes.selection
    act.keyboard.emitName(act, 'Delete')
    
def delete_PrevChar(act, withBackSpace=False):
	if withBackSpace:
		act.vibase.doc.backspace(act.pos.getIter(act), False, True)
	else:
		oldMode = act.bindings.mode
		act.bindings.mode = act.modes.visual
		act.pos.move_Backward(act, True)
		cut_Selection(act)
		act.bindings.mode = oldMode
    
def delete_Char(act,  withBackSpace=False):
    act.pos.move_Forward(act)
    delete_PrevChar(act, withBackSpace)

def delete_WholeLines(act):
    number = act.vibase.numLines
    act.lines.select_Lines(act, number)
    cut_Selection(act)
    cursor = act.pos.getIter(act)
    line = cursor.get_line()
    if line > 0:
        delete_PrevChar(act, withBackSpace=True)
        act.pos.move_Forward(act)
    else:
        delete_Char(act, withBackSpace=True)
        
def delete_ToLineEnd(act):
    act.lines.select_ToLineEnd(act)
    cut_Selection(act)
    
def delete_ToLineBegin(act):
    act.lines.select_ToLineBegin(act)
    cut_Selection(act)
    
########################
###
###   COPYING
###
########################

def yank_Line(act):
    number = act.vibase.numLines
    act.lines.select_Lines(act, number)
    yank_Selection(act)
    
def yank_UntilEndOfLine(act):
    act.lines.select_ToLineEnd(act)
    yank_Selection(act)
    
def yank_TillEndOfWord(act):
    select_ToWordEnd(act)
    yank_Selection(act)

def yank_NextWord(act):
    select_NextWord(act)
    yank_Selection(act)
    
def yank_ToLineEnd(act):
    act.lines.selectToLineEnd(act)
    yank_Selection(act)
    
def yank_Selection(act):
    act.vibase.view.copy_clipboard()
    
    
########################
###
###   PASTING
###
########################
    
def paste_ClipboardAbove(act):
    act.pos.move_LineBegin(act)
    act.vibase.view.paste_clipboard()
    act.keyboard.emitNewLine(act)

def paste_ClipboardBelow(act):
    act.pos.move_LineEnd(act)
    act.keyboard.emitNewLine(act)
    act.vibase.view.paste_clipboard()
    
    
########################
###
###   CUTTING
###
########################
    
def cut_Selection(act):
    act.vibase.view.cut_clipboard()
    
def cut_UntilEndOfLine(act):
    act.lines.select_ToLineEnd(act)
    cut_Selection(act)
    
def cut_Line(act):
    number = act.vibase.numLines
    act.lines.select_Lines(act, number)
    cut_Selection(act)
    
def cut_TillEndOfWord(act):
    select_ToWordEnd(act)
    cut_Selection(act)

def cut_NextWord(act):
    select_NextWord(act)
    cut_Selection(act)
    
########################
###
###   SELECTION
###
########################

def select_ToWordEnd(act):
    act.bindings.mode = act.modes.visual
    act.pos.move_WordForward(act)
    
def select_NextWord(act):
    act.pos.move_WordBackward(act)
    act.bindings.mode = act.modes.visual
    act.pos.move_WordForward(act)
    
########################
###
###   OTHER
###
########################

def getAll(act):
    start = act.vibase.doc.get_start_iter()
    end = act.vibase.doc.get_end_iter()
    return act.vibase.doc.get_text(start, end, False)


def setAll(act, new):
    start = act.vibase.doc.get_start_iter()
    end = act.vibase.doc.get_end_iter()
    return act.vibase.doc.set_text(new)
   
def switchChar(act):
	delete_Char(act)
	act.pos.move_Forward(act)
	act.menus['paste'].activate()
	act.bindings.mode = act.modes.insert

