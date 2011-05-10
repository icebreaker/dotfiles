import re
import os
import gedit
import gobject

########################
###
###   MANAGER
###
########################

class exManager(object):
    """Holds the regex->function combinations"""
    def __init__(self):
        self.registry = []
    
    def add(self, regex, function):
        self.registry.append((regex, function))
        
    def evaluate(self, act, command):
        act.trace.info(1, "\tEvaluating %s", command)
        index = act.vigtk.exOptions.index
        act.vigtk.exOptions.history.insert(index+1, "".join(act.vibase.stack))
        
        act.vigtk.exOptions.lastCommand = command
        act.vigtk.exOptions.index += 1
        try:
            for regex, function in self.registry:
                result = regex.match(command)
                if result:
                    act.bindings.mode = act.modes.command
                    act.trace.info(1, "\tex calling %s", function.__name__)
                    function(act, command, result)
                    raise StopIteration
            act.trace.info(1, "\tEx found no match")
            act.vibase.setExtraStatus(1, lambda act : " _____ INVALID command")
        except StopIteration:
            #already executed necessary function, can stop now
            pass

#This is to be used to execute commands in ex mode
#act.ex returns this
manager = exManager()

########################
###
###   DECORATOR
###
########################

class regexDec(object):
    """Decorator used to associate regex patterns with functions"""
    
    def __init__(self, regex, fullRegex=True):
        if fullRegex:
            regex = "^%s$" % regex

        self.regex = re.compile(regex)
    
    def __call__(self, f):
        manager.add(self.regex, f)
        return f

########################
###
###   REGEX/FUNCTION
###
########################

@regexDec("w")
def ex_Write(act, command, result):
    act.fileOps.saveFile(act)

@regexDec("wq")
def ex_WriteQuit(act, command, result):
    # Need to wait for file to finish saving
    act.fileOps.saveFile(act)
    gobject.timeout_add(100, act.fileOps.closeQuit, act)

@regexDec("q")
def ex_Quit(act, command, result):
    act.fileOps.closeTab(act, True)

@regexDec("tabnew")
def ex_NewTab(act, command, result):
    act.vigtk.window.create_tab(True)

@regexDec("nt")
def ex_NextTab(command, result):
    act.info(2, "Select next tab")

@regexDec("pt")
def ex_PrevTab(act, command, result):
    act.info(2, "Select previous tab")

@regexDec("q!")
def ex_QuitWithoutSaving(act, command, result):
    act.fileOps.closeTab(act, False)

@regexDec("tabnew (.+)")
def ex_OpenInTab(act, command, result):
    fileName = "%s/%s" % (act.fileOps.getCurrentFolder(act), result.group(1))
    if not act.vigtk.window.get_active_document().get_uri():
        act.vigtk.window.close_tab(act.vigtk.window.get_active_tab())
    act.vigtk.window.create_tab_from_uri(fileName, gedit.encoding_get_utf8(), 1, True, True)

@regexDec("sav (.+)")
def ex_SaveAs(act, command, result):
    act.trace.info(1, "TODO : make save as work properly")
    act.menus["saveAs"].activate()
    pass

@regexDec("(\d+)")
def ex_GotToLine(act, command, result):
    number = int(command)
    act.pos.goToLine(act, number)
    
@regexDec("e (.+)")
def ex_OpenInCurrentView(act, command, result):
    fileName = "%s/%s" % (act.fileOps.getCurrentFolder(act), result.group(1))
    act.vigtk.window.close_tab(act.vigtk.window.get_active_tab())
    act.vigtk.window.create_tab_from_uri(fileName, gedit.encoding_get_utf8(), 1, True, True)

@regexDec("!(.+)")
def ex_CommandForTerminal(act, command, result):
    terminalCommand = result.group(1)
    terminal = act.others.getTerminal(act)
    terminal._vte.feed_child(terminalCommand + "\n")

@regexDec("printall")
def ex_PrintAll(act, command, result):
    location = "%s/Desktop" % os.environ['HOME']
    act.others.printall(act, location)
    
@regexDec("printall (.+)")
def ex_PrintAllLoc(act, command, result):
    location = result.group(1)
    act.others.printall(act, location)

@regexDec(r's/(?P<search>(?:\\.|(?!/)[^\\])+)(/(?P<replace>(?:\\.|(?!/)[^\\])+)(/(?P<options>.+))?)?')
def ex_Search(act, command, result):
    search = result.groupdict()['search']
    replace = result.groupdict()['replace']
    options = result.groupdict()['options']
    
    validOptions = False
    if options:
        validOptions = all(letter in ('i', 'L', 'm', 's', 'u', 'x') for letter in options)
        if validOptions:
            search = "(?%s)%s" % (options, search)
        else:
            act.trace.warn("Options aren't valid, (must be 'i', 'L', 'm', 's', 'u' or 'x')")
            
    try:
        sre = re.compile(search)
    except:
        act.trace.error("search regex failed to compile : %s" % search)
        sre = None
    
    if (search and not sre) or (options and not validOptions):
        act.vibase.setExtraStatus(1, lambda act : " _____ ERRORS in search request")
    else:
        if not replace:
            act.trace.info(1, "\tSearching for %s", search)
            document = act.text.getAll(act)
            count = 0
            for m in sre.finditer(document):
                #need to determine how to highlight them
                act.trace.info(2, '\t%d-%d', m.start(), m.end())
                count += 1
            
            act.vibase.setExtraStatus(1, lambda act : " _____ FOUND %d instances" % count)
        else:
            act.trace.info(1, "\tSearching for %s, Replacing with %s", search, replace)
            document = act.text.getAll(act)
            newDocument, count = sre.subn(replace, document)
            act.text.setAll(act, newDocument)
            act.vibase.setExtraStatus(1, lambda act : " _____ REPLACED %d instances" % count)
    
    act.bindings.mode = act.modes.ex
    act.vibase.stack = list(command)
    act.vibase.setMessage(act)



    
