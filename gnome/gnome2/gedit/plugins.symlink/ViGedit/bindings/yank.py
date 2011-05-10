from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(None, act.gtk.keysyms.a)
        
        self.reg(self.nop, act.gtk.keysyms.B, after=(act.modes.block, ["yank", "numLines"]))
        self.reg(self.nop, act.gtk.keysyms.t, after=(act.modes.t,     ["yank", "numLines", "f"]))
        
        self.reg(act.text.yank_Line,          act.gtk.keysyms.y,      pos=True, after=act.modes.command, **self.fr)
        self.reg(act.text.yank_TillEndOfWord, act.gtk.keysyms.w,      pos=True, after=act.modes.command, **self.fr)
        self.reg(act.text.yank_NextWord,      act.gtk.keysyms.w,      pos=True, after=act.modes.command,
                                                                                              stack="a", **self.fr)
                                                                                              
        self.reg(act.text.yank_ToLineEnd,     act.gtk.keysyms.dollar, pos=True, after=act.modes.command, **self.fr)
