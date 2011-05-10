from ViGedit import static
from ViGedit.actions import act
modes = static.modes.getModes()
modules = {}

########################
###
###   REGISTRY
###
########################

class VIG_Registry(object):
    """Holds all the different bindings across all act.modes. Initiated once per instance of the plugin"""
    
    def __init__(self):
    
        #self.rego will be an object of modeName : bindings
        #Bindings will be another object of keycombo : bindingsObject
        #see register function for more info
        self.rego = {}
    
    def __getitem__(self, key):
        currentMode, keycode, control, meta, stack = key
        try:
            return self.rego[currentMode][keycode, control, meta, stack]
        except KeyError:
            return None
    
    def __setitem__(self, key, value):
        raise Exception, "Use the register function"
    
    def register(self, mode, function, keycode, control=False, meta=False,
                    final=False, repeat=False, after=None, pos=False,
                    ignoreStack=False, stack = "", recordAction = True):
        
        keycombo = keycode, control, meta, stack
        try:
            modeRegister = self.rego[mode]
        except KeyError:
            self.rego[mode] = {}
            modeRegister = self.rego[mode]
        
        try:
            alreadyRegistered = modeRegister[keycombo]
            raise Exception, "%s has already been registered" % keycombo
        except:
            #Hasn't been registered yet, let's register it now
            modeRegister[keycombo] = {
                'Function'      : function,
                'Final'         : final,
                'Repeatable'    : repeat,
                'AfterMode'     : after,
                'PreservePos'   : pos,
                'IgnoreStack'   : ignoreStack,
                'StackMatch'    : stack,
                'RecordAction'  : recordAction,
            }
        

registry = VIG_Registry()

########################
###
###   MODES
###
########################

class VIG_ModeHolder(object):
    """holds instances of all the modes"""
    def start(self):
        for mode in modes:
            try:
                next = modules["mode_%s" % mode]
            except KeyError:
                next = None
            
            if next:
                next = next.Mode(registry, mode)
                
                setattr(self, "mode_%s" % mode, next)
    
    def __getitem__(self, key):
        if key in modes:
            return getattr(self, "mode_%s" % key)
        else:
            raise Exception, "%s is not a valid mode" % key

vigm = VIG_ModeHolder()
    
########################
###
###   BINDINGS
###
########################

class VIG_Bindings(object):
    def __init__(self, act):
        """Allows access to the modes"""
        object.__setattr__(self, "act", act)
        object.__setattr__(self, "vigm", vigm)
        
    def __setattr__(self, key, value):
        """Used to set the current mode"""
        if key.lower() == "mode":
            if type(value) is str:
                self.setMode(value)
                
            elif type(value) in (list, tuple):
                self.setMode(*value)
                
            elif type(value) is dict:
                self.setMode(**value)
                
            else:
                raise Exception, "%s : Mode must be a string or a tuple/list/dict of type, option" % value
        else:
            raise Exception, "In the Registry, 'mode' is the only attribute you may change"
    
    def __getattr__(self, key):
        if key.lower() == "mode":
            return self.act.vibase.view.get_data("mode")
        else:
            object.__getattribute__(self, key)
    
    def setMode(self, mode, options=None):
        self.vigm[mode].introduce(self.act, options)
        self.act.vibase.view.set_data("mode", mode)
        self.act.vibase.update()

for mode in modes:
    try:
        exec "import %s as mode_%s" % (mode, mode)
        modules["mode_%s" % mode] = locals()["mode_%s" % mode]
    except ImportError:
        act.trace.warn("%s failed to import", mode)
        
vigm.start()


