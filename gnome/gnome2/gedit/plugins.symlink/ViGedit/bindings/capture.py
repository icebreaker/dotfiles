from base import VIG_ModeBase

class MODE_options(object):
    """Options object for this mode"""
    def __init__(self, act, options=None):
        self.captureNum = 0
        self.capturedEvents = []
        self.start = None
        self.capture = None
            
class Mode(VIG_ModeBase):

    """
        TODO :
                Ability to save the saved capture into a specific name (maybe even accessable across all tabs)
                Ability to load saved capture from a specific name
    """
    
    def setup(self, act):
        self.reg(self.captureNextEvents,      act.gtk.keysyms.a, final=True)
        self.reg(self.setCaptureMode,         act.gtk.keysyms.d, final=True, after=act.modes.command)
        self.reg(self.setStartMode,           act.gtk.keysyms.s, final=True, after=act.modes.command)
        self.reg(self.clearCapturedEvents,    act.gtk.keysyms.c, final=True, after=act.modes.command)
        self.reg(self.emitCapturedEvents,     act.gtk.keysyms.e, final=True)
    
    def extraStatus(self, act):
        options = act.vibase.captureOptions
        captureNum = options.captureNum
        capturedEvents = options.capturedEvents
        
        message = ""
        if captureNum > 0:
            if captureNum > 1:
                message = " ___ Capturing next %s key presses (%s caught)" % (captureNum, len(capturedEvents))
            else:
                message = " ___ Capturing last key press (%s caught)" % len(capturedEvents)
        return message
            
    def intro(self, act, options=None):
        VIG_ModeBase.intro(self, act, options)
        if not hasattr(act.vibase, "captureOptions"):
            #we want the options object to only be initialised once
            act.vibase.captureOptions = MODE_options(act, options)
    
    ########################
    ###   CAPTURE
    ########################
    
    def captureNextEvents(self, act):
        options = act.vibase.captureOptions
        num = int("".join(act.vibase.number or ['0']))
        act.vibase.setExtraStatus(num, self.extraStatus)
        options.captureNum = num
        
        act.bindings.mode = act.modes.command
        if options.capture:
            options.captureNum += 1
            act.keyboard.emitEvent(act, options.capture)
        
        def capture(act, event):
            options = act.vibase.captureOptions
                
            if options.captureNum > 0:
                capturedEvent = act.keyboard.makeEvent(act, event.keyval, event.state)
                options.capturedEvents.append(capturedEvent)
                options.captureNum -= 1
                
        act.vibase.setRule(num, capture)
    
    ########################
    ###   GET START MODE
    ########################
    
    def setFutureMode(self, act, when, message):
        act.bindings.mode = act.modes.command
        act.vibase.setExtraStatus(1, lambda act : " (%s)" % message)
        
        def getEvent(act, event, when):
            if type(when) is str:
                when = (when, )
            
            for w in when:
                setattr(act.vibase.captureOptions, w, act.keyboard.makeEvent(act, event.keyval, event.state))
            
        act.vibase.setRule(1, lambda a, e : getEvent(a, e, when))
    
    def setStartMode(self, act):
        when = "start"
        if not act.vibase.captureOptions.capture:
            when = [when, 'capture']
            
        self.setFutureMode(act, when, "next key determines start mode when emitting captured keys")
    
    def setCaptureMode(self, act):
        self.setFutureMode(act, 'capture', "Next key determines mode for capturing keys")
    
    ########################
    ###   EMIT
    ########################
    
    def emitCapturedEvents(self, act):
        options = act.vibase.captureOptions
        act.bindings.mode = act.modes.command
        if options.start:
            act.keyboard.emitEvent(act, options.start)
            
        message = "captured keys : ["
        for event in options.capturedEvents:
            act.keyboard.emitEvent(act, event)
            message += "%s " % unichr(act.gdk.keyval_to_unicode(event.keyval))
                
        act.trace.info(1, "%s]", message)
    
    ########################
    ###   CLEAR
    ########################
    
    def clearCapturedEvents(self, act):
        options = act.vibase.captureOptions
        options.capturedEvents = []
        options.captureNum = 0
        options.start = None
        options.capture = None
        
