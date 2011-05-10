from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(None, act.gtk.keysyms.a)
        
        self.reg(self.nop, act.gtk.keysyms.B, after=(act.modes.block, ["change", "numLines"]))
        self.reg(self.nop, act.gtk.keysyms.t, after=(act.modes.t,     ["change", "numLines", "f"]))
        
        self.reg(act.text.cut_TillEndOfWord,  act.gtk.keysyms.w, after=act.modes.insert, **self.fr)
        self.reg(act.text.cut_NextWord,       act.gtk.keysyms.w, after=act.modes.insert, stack="a", **self.fr)
        self.reg(act.text.cut_Line,           act.gtk.keysyms.l, after=act.modes.insert, stack="a", **self.fr)
