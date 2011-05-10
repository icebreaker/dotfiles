from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(None, act.gtk.keysyms.a)
        
        self.reg(self.nop, act.gtk.keysyms.B, after=(act.modes.block, ["delete", "numLines"]))
        self.reg(self.nop, act.gtk.keysyms.t, after=(act.modes.t,     ["delete", "numLines", "f"]))
        
        self.reg(act.text.delete_WholeLines,  act.gtk.keysyms.d,           after=act.modes.command,      **self.fr)
        self.reg(act.text.delete_ToLineEnd,   act.gtk.keysyms.dollar,      after=act.modes.command,      **self.fr)
        self.reg(act.text.delete_ToLineBegin, act.gtk.keysyms.asciicircum, after=act.modes.command,      **self.fr)
        self.reg(act.text.cut_TillEndOfWord,  act.gtk.keysyms.w,           after=act.modes.command,      **self.fr)
        self.reg(act.text.cut_NextWord,       act.gtk.keysyms.w,           after=act.modes.command, stack="a",**self.fr)

