from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(act.pos.move_Backward, act.gtk.keysyms.BackSpace, final=True)

    def handle(self, act, event):
        if not act.keyboard.isModifierPressed(act, event):
            act.vibase.addToStack(event)
            act.vibase.setOverwrite(True)
            return False
