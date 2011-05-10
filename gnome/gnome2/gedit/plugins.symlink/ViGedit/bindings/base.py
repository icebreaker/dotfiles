from ViGedit.actions import act

class VIG_ModeBase(object):
    """Every mode must inherit from this"""
    
    def __init__(self, registry, mode):
        self.registry = registry
        self.mode = mode
        self.fr = {"final":True, "repeat" :True}
        self.setup(act)
    
    def setup(self, act):
        """Used to setup any bindings"""
        pass
    
    def introduce(self, act, options=None):
        """Called when the current mode is set to this"""
        self.intro(act, options)
        self.trace(act)
        self.status(act)
    
    def intro(self, act, options=None):
        """Setup when introduced"""
        act.vibase.stack = []
        act.vibase.select = False
        act.vibase.view.emit("select-all", False)
        pass
    
    def trace(self, act):
        """Trace to the terminal when introduced"""
        act.trace.intro(self)
    
    def status(self, act):
        """Display this in the statusbar"""
        return "%s Mode" % self.mode.capitalize()
    
    def handle(self, act, event):
        """Called when no binding has been found and so the mode is left to handle the event"""
        return True
    
    def ignore(self, vibase, event):
        """Returns True if this event should be ignored"""
        return False
    
    def nop(self, act):
        pass

    def reg(self, *args, **kwargs):
        self.registry.register(self.mode, *args, **kwargs)
