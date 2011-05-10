def append_After(act):
    cursor = act.pos.getIter(act)
    if cursor.ends_line():
        act.vibase.doc.insert_at_cursor(" ")
    else:
        act.pos.move_Forward(act)
    return True
    
def insert_BeginLine(act):
    cursor = act.pos.getIter(act)
    cursor.backward_sentence_start()
    act.vibase.doc.place_cursor(cursor)
    
def open_LineAbove(act):
    act.pos.move_LineBegin(act)
    act.bindings.mode = act.modes.insert
    act.keyboard.emitNewLine(act)
    act.pos.move_Up(act)

def open_LineBelow(act):
    act.pos.move_LineEnd(act)
    act.bindings.mode = act.modes.insert
    act.keyboard.emitNewLine(act)
