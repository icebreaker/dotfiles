from ViGedit import static
from ViGedit import keyboard
from ViGedit import cursor
import gtk
from gtk import gdk
modules = {}

class VIG_Actions(object):
    """Middleman to all the actions functions"""
    
    def __init__(self, vibase):
        self.vibase = vibase
        if vibase:
            self.vigtk = self.vibase.vigtk
    
    #I'm lazy, I don't want to write the quotations around all of them :p
    MODULES = "blocks fileOperations insert lines others text ex trace".split(" ")
    
    def __getattr__(self, key):
        
        try:
            #these ones are the names of the module, but we don't want the module to be returned
            return {
                'ex' : modules["ex"].manager
            }[key.lower()]
        except KeyError:
            pass
        
        try:
            return modules[key.lower()]
        except KeyError:
            #Musn't be a module, let's try the other options now
            pass
        
        try:
            #names that aren't modules, but we want something to return from it
            #that don't refer to the currently active instance of vibase
            return {
                'fileops'           : modules["fileOperations"],
                'static'            : static,
                'modes'             : static.modes,
                'keyboard'          : keyboard.instance,
                'pos'               : cursor.instance,
                'gtk'               : gtk,
                'gdk'               : gdk,
                'getmenu'           : lambda menu : lambda act : act.menus[menu].activate(),
            }[key.lower()]
        except KeyError:
            if self.vibase is None:
                raise Exception, "No such actions group as %s whilst still registering" % key.lower()
        
        try:
            #names that aren't modules, and refer to something in the current active instance of vibase
            return {
                'vibase'            : self.vibase,
                'doc'               : self.vibase.doc,
                'bindings'          : self.vibase.bindings,
                'mode'              : self.vibase.bindings.mode,
                'vigtk'             : self.vigtk,
                'menus'             : self.vigtk.menus,
            }[key.lower()]
            
        except KeyError:
            raise Exception, "No such actions group as %s" % key.lower()

for module in VIG_Actions.MODULES:
    exec "import %s" % module
    m = locals()[module]
    modules[module] = m
    
#Only to be used by the setup function of the modes in the bindings folder
act = VIG_Actions(None)
   
