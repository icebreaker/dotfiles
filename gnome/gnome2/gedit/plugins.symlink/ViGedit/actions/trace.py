from ViGedit.options import opts
from gtk import gdk

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[1m\033[92m'
WARNING = '\033[43m'
MAGNETA = '\033[95m'
ERROR = '\033[91m'
ENDC = '\033[0m'


    
def error(message, *args):
    if opts.TraceLevel > 1:
        print "%sError : %s%s" % (ERROR, message % args, ENDC)
def warn(message, *args):
    if opts.TraceLevel > 2:
        print "%sWarning : %s%s" % (WARNING, message % args, ENDC)

def info(level, message, *args, **kwargs):
    if 'color' not in kwargs:
        if level == 1:
            color = GREEN
        else:
            color = BLUE
    else:
        color = kwargs['color']
    if opts.TraceLevel > (level + 1) or opts.TraceLevel < -level:
        print "%s%s%s" % (color, message % args, ENDC)

def keyPress(event):
    if opts.TraceKeys:
        print "%s : %s pressed" % (event.keyval, gdk.keyval_name(event.keyval))

def intro(mode=None, message=None, *args):
    if message:
        info(1, message, *args, **{'color' : MAGNETA})
    else:
        info(1, "Introducing %s mode", mode.mode, **{'color' : MAGNETA})
        
    
