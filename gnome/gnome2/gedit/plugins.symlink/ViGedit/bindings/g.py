from base import VIG_ModeBase

class Mode(VIG_ModeBase):
    
    def setup(self, act):
        self.reg(act.pos.move_BufferTop,    act.gtk.keysyms.g,          after=act.modes.command,  **self.fr)
        self.reg(self.nextTab,              act.gtk.keysyms.t,          after=act.modes.command,  **self.fr)
        
    def nextTab(self, act):
        documents = act.vigtk.window.get_documents()
        thisDocument = act.vigtk.window.get_active_document()
        i = None
        for iterator, document in enumerate(documents):
            if document == thisDocument:
                i = iterator + 1
            elif iterator == i:
                act.vigtk.window.set_active_tab(act.vigtk.window.get_tab_from_uri(documents[i].get_uri()))
            elif i == None:
                act.vigtk.window.set_active_tab(act.vigtk.window.get_tab_from_uri(documents[0].get_uri()))
      
      
      
