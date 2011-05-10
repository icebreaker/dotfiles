from base import VIG_ModeBase
class StopLoop(Exception):pass

class MODE_options(object):
    def reset(self, act, options = None):
        try:
            theOption, numTimes, direction = options
            other = None
        except ValueError:
            theOption, numTimes, direction, other = options
            try:
                other = chr(act.gdk.keyval_from_name(other))
            except ValueError:
                act.trace.warn("failed to use chr() on %s", act.gdk.keyval_from_name(other))
        
        if type(numTimes) is str:
            numTimes = getattr(act.vibase, numTimes)
            
            if type(numTimes) in (list, tuple):
                try:
                    numTimes = int("".join(numTimes or ['1']))
                except ValueError:
                    numTimes = 1
        
        self.option = theOption
        self.numTimes = numTimes
        self.direction = direction
        self.other = other
    
    def __str__(self):
        return "%s %s %d times" % (self.option, {'f' : 'Forward', 'b' : 'Backward'}[self.direction], self.numTimes)
            
class Mode(VIG_ModeBase):
    
    def trace(self, act):
        options = act.vibase.tOptions
        act.trace.intro(self.mode, "introducing %s mode (%s)", self.mode, options)
        
    def status(self, act):
        options = act.vibase.tOptions
        
        message = VIG_ModeBase.status(self, act)
        if options:
            message += " (%s)" % options.option
        
        return message
        
    def intro(self, act, options=None):
        VIG_ModeBase.intro(self, act, options)
        if not hasattr(act.vibase, 'tOptions'):
            optionsInstance = MODE_options()
            act.vibase.tOptions = optionsInstance
        else:
            optionsInstance = act.vibase.tOptions
        
        optionsInstance.reset(act, options)
    
    def handle(self, act, event):
        """ moves cursor to next occurance of the next key to be pressed """
        options = act.vibase.tOptions
        cursor = act.pos.getIter(act)
        origin = cursor.copy()
        
        count = 0
        try:
            wanted = chr(event.keyval)
        except ValueError:
            wanted = None
        
        numTimes = options.numTimes
        if wanted:
            try:
                while True:
                    count+=1
                    
                    if options.direction == "f":
                        if cursor.is_end():
                            act.trace.info(2, "cursor at end")
                            raise StopLoop
                        
                        cursor.forward_char()
                        char = cursor.get_char()
                        act.trace.info(2, "f%s : %s : %s : %s", numTimes, char, wanted, char==wanted)
                        
                        if char == wanted:
                            if numTimes > 1 :
                                numTimes -= 1
                            else :
                                act.trace.info(2, "going forward, numtimes is 1, found %s", wanted)
                                raise StopLoop
                        elif char == options.other:
                            numTimes += 1
                        
                    elif options.direction == "b" :
                        if cursor.is_start():
                            act.trace.info(2, "cursor at start")
                            raise StopLoop
                        
                        cursor.backward_char()
                        char = cursor.get_char()
                        act.trace.info(2, "b%d : %s : %s : %s", numTimes, char, wanted, char==wanted)
                        
                        if char == wanted:
                            if numTimes > 1 :
                                numTimes -= 1
                            else :
                                act.trace.info(2, "going backward, numtimes is 1, found %s", wanted)
                                raise StopLoop
                        elif char == options.other:
                            numTimes += 1
            except StopLoop:
                act.trace.info(2, "loop stopped")
                pass
               
            if options.option == "find" :
                if not cursor.is_end():
                    act.vibase.doc.place_cursor(cursor)
                act.bindings.mode = act.modes.command
            else :
                act.bindings.mode = act.modes.visual
                act.pos.move_Forward(act, count)
                
                if options.option == "change" :
                    act.text.cut_Selection(act)
                    act.bindings.mode = act.modes.insert
                    
                elif options.option == "delete" :
                    act.text.cut_Selection(act)
                    act.bindings.mode = act.modes.command
                
                elif options.option == "yank" :
                    act.text.yank_Selection(act)
                    act.bindings.mode = act.modes.command
                    act.pos.moveInsert(act, origin)
                
            return True
            
        return False
