from base import VIG_ModeBase

class Mode(VIG_ModeBase):

    def intro(self, act, options):
        act.vibase.stack = []
        act.vibase.select = False
        
    def handle(self, act, event):
        if act.keyboard.isDirectionalPressed(act, event):
            act.bindings.mode = act.modes.command
            return False
        
        elif event.keyval == act.gtk.keysyms.Tab:
            return False
        
        elif act.keyboard.isModifierPressed(act, event) == False:
            try:
                start, end = act.vibase.doc.get_selection_bounds()
            except ValueError:
                return True
            
            act.vibase.addToStack(event)
            act.vibase.doc.delete(start, end)
            act.bindings.mode = act.modes.insert
            return event.keyval in (act.gtk.keysyms.BackSpace, act.gtk.keysyms.Delete)
        else:
            return False
