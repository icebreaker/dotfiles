from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(act.lines.indentLeft,  act.gtk.keysyms.less,     after=act.modes.command, **self.fr)
        self.reg(act.lines.indentRight, act.gtk.keysyms.greater,  after=act.modes.command, **self.fr)
