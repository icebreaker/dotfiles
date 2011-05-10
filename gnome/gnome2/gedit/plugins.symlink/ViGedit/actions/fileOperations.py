import gedit, gobject, os

def saveFile(act):
    if act.vibase.doc.get_uri() != None:
        act.menus["save"].activate()
    else:
        act.menus["saveAs"].activate()

def closeTab(act, save = True):
    if save and act.vigtk.window.get_active_document().get_modified():
        act.menus["fileClose"].activate()
    else:
        act.vigtk.window.close_tab(act.vigtk.window.get_active_tab())
        
    gobject.timeout_add(100, waitUntilDialogDone, act)

def waitUntilDialogDone(act):
    if act.vigtk.window.get_active_tab() and act.vigtk.window.get_active_document().get_modified():
        act.trace.info(2, "Window still saving...")
        return True
    else:
        act.trace.info(1, "Window done saving!")
        tab = act.vigtk.window.get_active_tab()
        if tab:
            if tab.get_state() == gedit.TAB_STATE_CLOSING:
                return True
        if act.vigtk.window.get_views() == []:
            act.trace.info(1, "No more views left, so shutting down!")
            # This gives messy messages.
            act.menus["quit"].activate()
            act.gtk.main_quit()
        return False

def closeQuit(act):
    tab = act.vigtk.window.get_active_tab()
    if tab.get_state() == gedit.TAB_STATE_SAVING:
        return True
    else:
        closeTab(act)
        return False
    
def getCurrentFolder(act):
    uri = act.vibase.doc.get_uri()
    if uri:
        return os.sep.join(uri.split(os.sep)[:-1])
    else:
        return os.cwd()
