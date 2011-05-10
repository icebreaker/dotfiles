from base import VIG_ModeBase

class MODE_options(object):
    """Options object for this mode"""
    def reset(self, act, options=None):
        theOption, numTimes = options
        
        if type(numTimes) is str:
            numTimes = getattr(act.vibase, numTimes)
            
            if type(numTimes) in (list, tuple):
                try:
                    numTimes = int("".join(numTimes or ['1']))
                except ValueError:
                    numTimes = 1
        
        self.option = theOption
        self.numTimes = numTimes
    
    def __str__(self):
        return self.option
        
class Mode(VIG_ModeBase):
        
    def trace(self, act):
        options = act.vibase.blockOptions
        act.trace.intro(self.mode, "Introducing %s mode (%s)", self.mode, options)
    
    def status(self, act):
        options = act.vibase.blockOptions
        
        message = VIG_ModeBase.status(self, act)
        if options:
            message += " (%s)" % options.option
        
        return message
            
    def intro(self, act, options=None):
        VIG_ModeBase.intro(self, act, options)
        if not hasattr(act.vibase, 'blockOptions'):
            optionsInstance = MODE_options()
            act.vibase.blockOptions = optionsInstance
        else:
            optionsInstance = act.vibase.blockOptions
        
        optionsInstance.reset(act, options)
    
    def handle(self, act, event):
        """do something with specified block"""
        options = act.vibase.blockOptions
        option = options.option
        numTimes = options.numTimes
        
        cursor = act.pos.getIter(act)
        origin = cursor.copy()
        count = 0
        try:
            wanted = act.gdk.keyval_name(event.keyval)
        except ValueError:
            wanted = None
            
        if wanted:
            try:
                other = {
                    'braceleft'   : 'braceright',
                    'parenleft'   : 'parenright',
                    'bracketleft' : 'bracketright',
                    "quotedbl"    : "quotedbl",
                    'apostrophe'  : 'apostrophe',
                }[wanted]
            except KeyError:
                act.trace.warn("%s not part of a pair", wanted)
                other = None
        
        if wanted and other:
            
            try:
                action = {
                    'select' : lambda : act.blocks.selectWhole(act, wanted, other),
                    'change' : lambda : act.blocks.changeWhole(act, wanted, other),
                    'delete' : lambda : act.blocks.deleteWhole(act, wanted, other),
                    'yank'   : lambda : act.blocks.yankWhole(act, wanted, other),
                }[option]()
                
                if option == 'yank':
                    act.pos.moveInsert(act, origin)
                    
                return True
            except KeyError:
                act.trace.warn("%s is not a valid option", option)
                pass
            
        return False
