from base import VIG_ModeBase

class Mode(VIG_ModeBase):

    def intro(self, act, options=None):
        act.vibase.setOverwrite(False)
        act.vibase.view.emit("select-all", False)
        act.vibase.stack = []
        act.vibase.select = False
