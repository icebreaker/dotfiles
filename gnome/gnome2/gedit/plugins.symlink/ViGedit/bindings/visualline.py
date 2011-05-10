from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(self.nop,                      act.gtk.keysyms.i,           after=act.modes.insert)
        self.reg(self.nop,                      act.gtk.keysyms.B,           after=(act.modes.block, ["select", "number"]))
        self.reg(self.nop,                      act.gtk.keysyms.t,           after=(act.modes.t,     ["select", "number", "f"]))

        self.reg(act.getmenu('cut'),            act.gtk.keysyms.x,           after=act.modes.command, final=True)
        self.reg(act.getmenu('copy'),           act.gtk.keysyms.y,           after=act.modes.command, final=True)
        self.reg(act.getmenu('paste'),          act.gtk.keysyms.p,           after=act.modes.command, final=True)
        self.reg(act.getmenu('selectAll'),      act.gtk.keysyms.a,           final=True)
                
        self.reg(act.pos.move_Forward,          act.gtk.keysyms.l,           **self.fr)
        self.reg(act.pos.move_Forward,          act.gtk.keysyms.Right,       **self.fr)
        self.reg(act.pos.move_Up_Lines,         act.gtk.keysyms.k,           **self.fr)
        self.reg(act.pos.move_Up_Lines,         act.gtk.keysyms.Up,          **self.fr)
        self.reg(act.pos.move_Backward,         act.gtk.keysyms.Left,        **self.fr)
        self.reg(act.pos.move_Backward,         act.gtk.keysyms.h,           **self.fr)
        self.reg(act.pos.move_Down_Lines,       act.gtk.keysyms.j,           **self.fr)
        self.reg(act.pos.move_Down_Lines,       act.gtk.keysyms.Down,        **self.fr)

        self.reg(act.pos.move_LineEnd,          act.gtk.keysyms.dollar,      final=True)
        self.reg(act.pos.move_LineEnd,          act.gtk.keysyms.End,         final=True)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.Home,        final=True)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.percent,     final=True)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.asciicircum, final=True)
        self.reg(act.pos.move_BufferEnd,        act.gtk.keysyms.G,           final=True)
        self.reg(act.pos.move_WordForward,      act.gtk.keysyms.w,           **self.fr)
        self.reg(act.pos.move_WordBackward,     act.gtk.keysyms.b,           **self.fr)
        
        self.reg(act.others.undo,               act.gtk.keysyms.u,           **self.fr)
        self.reg(act.others.search,             act.gtk.keysyms.slash,       final=True)

        self.reg(act.lines.indentLeft,          act.gtk.keysyms.less,        after=act.modes.visual,  **self.fr)
        self.reg(act.pos.move_LineEnd,          act.gtk.keysyms.A,           after=act.modes.insert,  **self.fr)
        self.reg(act.lines.indentRight,         act.gtk.keysyms.greater,     after=act.modes.visual,  **self.fr)
        self.reg(act.pos.move_LineBegin,        act.gtk.keysyms.I,           after=act.modes.insert,  **self.fr)
        self.reg(act.text.delete_PrevChar,      act.gtk.keysyms.X,           after=act.modes.command, final=True)
        self.reg(act.text.delete_Selection,     act.gtk.keysyms.d,           after=act.modes.command, final=True)
        self.reg(act.insert.open_LineAbove,     act.gtk.keysyms.O,           after=act.modes.visual,  **self.fr)
        self.reg(act.insert.open_LineBelow,     act.gtk.keysyms.o,           after=act.modes.visual,  **self.fr)

        self.reg(act.text.select_NextWord,        act.gtk.keysyms.w,           stack="s", **self.fr)

    def intro(self, act, options=None):
        act.vibase.stack = []
        act.vibase.select = True
    
    def handle(self, act, event):
        """ if a modifier is pressed, let it pass through so it can be registered by gedit
        (so you can still use ordinary shortcuts in visual mode) """
        return not act.keyboard.isModifierPressed(act, event)
    
    
        
