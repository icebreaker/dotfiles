########################
###
###   SELECT WHOLE
###
########################

def select_Line(act):
    select_OneLine(act)

def select_Lines(act, number):
    if act.mode == act.modes.visual:
        act.bindings.mode = act.modes.command
    if number > 1:
        select_ManyLines(act, number)
    else:
        select_OneLine(act)
        
def select_OneLine(act):
    
    if act.mode == act.modes.visual:
        act.bindings.mode = act.modes.command
        
    act.pos.move_LineBegin(act)
    
    cursor = act.pos.getIter(act)
    l1 = cursor.get_line()
    cursor.forward_line()
    if cursor.get_line() != l1:
        cursor.backward_char()
    
    act.pos.moveInsert(act, cursor, True)
        
def select_ManyLines(act, number):

    if act.mode == act.modes.visual:
        act.bindings.mode = act.modes.command
        
    if type(number) in (list, tuple):
        try:
            number = int("".join(number))
        except ValueError:
            number = 0
    
    act.pos.move_LineBegin(act)
    cursor = act.pos.getIter(act)
    l1 = cursor.get_line()
    cursor.forward_lines(number)
    l2 = cursor.get_line()
    if abs(l1 - l2) == number:
        cursor.backward_char()
        
    act.pos.moveInsert(act, cursor, True)
        
def getLinesTillEnd(act):
    """ determine how many lines from current position to the end of the file """
    cursor = act.pos.getIter(act)
    line = cursor.get_line()
    total = act.vibase.doc.get_line_count()
    act.trace.info(2, "lines till end of document : ", total-line)
    return total-line
    
########################
###
###   SELECT PART
###
########################

def select_ToLineEnd(act):
    act.bindings.mode = act.modes.visual
    act.pos.move_LineEnd(act)
    
def select_ToLineBegin(act):
    act.bindings.mode = act.modes.visual
    act.pos.move_LineBegin(act)
    
########################
###
###   OTHER
###
########################
    
def indentLeft(act):
    indent(act, "Left")

def indentRight(act):
    indent(act, "Right")

def indent(act, direction):
    numLines = act.vibase.numLines
    
    cursor = act.pos.getIter(act)
    select_Lines(act, numLines)
        
    if act.menus["indent%s" % direction] is not None:
        act.menus["indent%s" % direction].activate()
    else:
        print 'TODO: call custom/gtk indent method'
        
    act.pos.moveInsert(act, cursor)
    
    
    
    
