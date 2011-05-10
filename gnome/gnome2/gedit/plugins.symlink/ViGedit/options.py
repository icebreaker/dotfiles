class Options(object):
    def __init__(self):
        """Set default options here"""
        
        """
            TraceLevel determines what gets printed
            
             0 = nothing
             1 = only error messages
             2 = error and warning messages
             3 = error, warning and level 1 info
             4 = error, warning, level1 and level 2 info
             
             -1 = only level 1 info
             -2 = only level 2 info
             -3 = only level 1 and 2 info
        """
        self.TraceLevel = 3

        #TraceKeys determines whether or not to print captured keys
        self.TraceKeys = False

        #Determine if we use selection or visual mode when you select text in command mode
        self.useSelectionMode = False
    
    def load(self, path):
        """Given the path to some file, read in the file and ovverride settings on self"""
        pass
    
    def paths(self):
        """Yield any paths to get settings from here"""
        if False:
            yield ""
            
    def readSettings(self):
        """Read any user defined settings here
        i.e. look in ~/.vigedit or something"""
        for path in self.paths():
            self.load(path)

opts = Options()
