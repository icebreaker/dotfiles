########################
###
###   SELECTION
###
########################

def selectWhole(act, type1, type2):
    act.bindings.mode = act.modes.t, ["find", 1, "b", type2]
    act.keyboard.emitName(act, type1)

    act.pos.move_Forward(act)
    act.bindings.mode = act.modes.t, ["select", 1, "f", type1]
    act.keyboard.emitName(act, type2)
    
    act.bindings.mode = act.modes.selection
    
def selectTill(act, type1):
    act.bindings.mode = act.modes.t, ["select",1, "f"]
    act.keyboard.emitName(act, type1)
    act.bindings.mode = act.modes.selection
    
    
########################
###
###   CHANGE
###
########################

def changeWhole(act, type1, type2):
    selectWhole(act, type1, type2)
    act.text.cut_Selection(act)
    act.bindings.mode = act.modes.insert
    if type1 == "braceleft" and type2 == "braceright":
        openBlock(act)
    
def changeTill(act, type1):
    selectTill(act, type1)
    act.text.cut_Selection(act)
    act.bindings.mode = act.modes.insert
    
########################
###
###   DELETE
###
########################

def deleteWhole(act, type1, type2):
    selectWhole(act, type1, type2)
    act.text.cut_Selection(act)
    if type1 == "braceleft" and type2 == "braceright":
        act.bindings.mode = act.modes.insert
        openBlock(act)
    act.bindings.mode = act.modes.command
    
def deleteTill(act, type1):
    selectTill(act, type1)
    act.text.cut_Selection(act)
    act.bindings.mode = act.modes.command
    
########################
###
###   YANK
###
########################

def yankWhole(act, type1, type2):
    selectWhole(act, type1, type2)
    act.text.yank_Selection(act)
    act.bindings.mode = act.modes.command
    
def yankTill(act, type1):
    selectTill(act, type1)
    act.text.yank_Selection(act)
    act.bindings.mode = act.modes.command
    
########################
###
###   OTHER
###
########################

def openBlock(act):
    act.keyboard.emitNames(act, "Return", "Return", "Up", "Tab")
    
    
