from base import VIG_ModeBase
import os
import glob
import re

class MODE_options(object):
    """Options object for this mode"""
    def __init__(self, act, options=None):
        self.lastCommand = None
        self.history = []
        self.index = -1

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(self.evaluateEx,           act.gtk.keysyms.Return,    ignoreStack=True)
        self.reg(self.evaluateEx,           act.gtk.keysyms.KP_Enter,  ignoreStack=True)
        self.reg(self.cycleCompletions,     act.gtk.keysyms.Tab)
        self.reg(self.cycleHistoryBackward, act.gtk.keysyms.Up,        ignoreStack=True)
        self.reg(self.cycleHistoryForward,  act.gtk.keysyms.Down,      ignoreStack=True)
        self.reg(self.cycleHistoryEnd,      act.gtk.keysyms.Page_Down, ignoreStack=True)
        self.reg(self.cycleHistoryStart,    act.gtk.keysyms.Page_Up,   ignoreStack=True)
    
    def status(self, act):
        if act.vibase.stack:
            return ":" + "".join(act.vibase.stack)
        else:
            return "%s (start typing command)" % VIG_ModeBase.status(self, act)
            
    def intro(self, act, options=None):
        VIG_ModeBase.intro(self, act, options)
        #I want the history to survive for the entire window
        if not hasattr(act.vigtk, "exOptions"):
            #we want the options object to only be initialised once
            act.vigtk.exOptions = MODE_options(act, options)
        
    def handle(self, act, event):
        options = act.vigtk.exOptions
        if event.keyval == act.gtk.keysyms.BackSpace:
            if act.vibase.stack:
                act.vibase.stack.pop()
                
        if event.keyval == act.gtk.keysyms.Escape:
            act.bindings.mode = act.modes.command
            
        elif event.keyval not in (act.gtk.keysyms.Return, act.gtk.keysyms.BackSpace):
            act.vibase.addToStack(event)
        return True
    
    def cycleHistoryBackward(self, act):
        options = act.vigtk.exOptions
        command = "".join(act.vibase.stack)
        if command and command != options.lastCommand :
            if options.index == 0:
                options.history.insert(0, command)
            else:
                options.history.insert(options.index+1, command)
            options.lastCommand = command
        
        if not act.vibase.stack:
            act.vibase.stack = list(options.history[options.index])
            
        elif options.index > 0:
            options.index -= 1
            options.lastCommand = options.history[options.index]
            act.vibase.stack = list(options.history[options.index])
            
    def cycleHistoryForward(self, act):
        options = act.vigtk.exOptions
        command = "".join(act.vibase.stack)
        if command and command != options.lastCommand :
            options.history.insert(options.index+1, command)
            options.lastCommand = command
            options.index += 1
            
        if options.index < (len(options.history)-1):
            options.index += 1
            options.lastCommand = options.history[options.index]
            act.vibase.stack = list(options.history[options.index])
    
    def cycleHistoryStart(self, act):
        options = act.vigtk.exOptions
        command = "".join(act.vibase.stack)
        if command and command != options.lastCommand :
            if options.index == 0:
                options.history.insert(0, command)
            else:
                options.history.insert(options.index+1, command)
            options.lastCommand = command
        
        if options.index != 0:
            options.index = 0
            options.lastCommand = options.history[options.index]
            act.vibase.stack = list(options.history[options.index])
            
    def cycleHistoryEnd(self, act):
        options = act.vigtk.exOptions
        command = "".join(act.vibase.stack)
        if command and command != options.lastCommand :
            options.history.insert(options.index+1, command)
            options.lastCommand = command
            options.index += 1
            
        if options.index < (len(options.history)-1):
            options.index = len(options.history)-1
            options.lastCommand = options.history[options.index]
            act.vibase.stack = list(options.history[options.index])

    def cycleCompletions(self, act, up = True):
        act.trace.info(1, "TODO : make tab completion work")
        #I didn't like the previous code for this and removed it
        #At some point I'll come back and reimplement tab completion
        #unless someone else does it for me :p
        
    def evaluateEx(self, act):
        command = "".join(act.vibase.stack)
        act.trace.info(1, "evaluating expression %s" % command)
        act.ex.evaluate(act, command)
            
              
