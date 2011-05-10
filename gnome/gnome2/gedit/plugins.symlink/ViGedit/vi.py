# -*- coding: utf-8 -*-

#  vigtk.py -   holds the vibase class, which is instantiated
#               for every tab of every gedit window
#
#  Copyright (C) 2008 - Joseph Method
#  Copyright (C) 2008, 2009 - Stephen Moore
#  Copyright (C) 2006 - Trond Danielsen
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import static
import gtk
from gtk import gdk
from gobject import GObject

from ViGedit.bindings import VIG_Bindings
from ViGedit.actions import VIG_Actions
from ViGedit.options import opts

class VIG_Vibase(GObject):
    """Glues everything together"""
    
    def __init__(self, vigtk, view):
        self.vigtk = vigtk
        
        self.view = view
        self.doc = view.get_buffer()
            
        self.act = VIG_Actions(self)
        self.bindings = VIG_Bindings(self.act)
        
        self.cursor = self.act.pos
        self.keyboard = self.act.keyboard
        
        self.stack = []
        self.number = []
        self.rules = []
        
        self.numLines = 0
        self.extraMessageLife = 0
        self.returnToMode = None
        self.extraMessage  = None
        self.select = False
        self.lastOperation = None
        
        self.viewEvents = [
            self.view.connect("key-press-event", self.onKeyPress),
            self.view.connect("button-release-event", self.onButtonRelease),
        ]
        
        self.docEvents = [
            self.doc.connect("saved", self.updateDoc),
            self.doc.connect("loaded", self.updateDoc),
        ]
        
        self.setMessage()
    
    ########################
    ###   UTILITY
    ########################
    
    def setMessage(self, message=None):
        status = self.bindings.vigm[self.bindings.mode].status(self.act)
        if self.extraMessageLife > 0:
            status += self.extraMessage(self.act)
        self.vigtk.statusbar.update(status)

    def setExtraStatus(self, life, func):
        if life > 0:
            self.extraMessageLife = life
            self.extraMessage = func
        
    def setRule(self, life, func):
        self.rules.append((life, func))
    
    def addToStack(self, event):
        if event.keyval in range(256):
            self.stack.append(chr(event.keyval))
            
    def setOverwrite(self, boolean):
        if self.view.get_overwrite() != boolean:
            self.act.trace.info(2, "Setting overwrite to %s from %s", boolean, self.view.get_overwrite())
            self.view.emit("toggle-overwrite")
    
    def resetNumber(self):
        self.number = ['0']
    
    ########################
    ###   UPDATE/DEACTIVATE
    ########################
    
    def update(self):
        self.setMessage()
        
    def updateDoc(self, doc, view):
        self.update()
    
    def deactivate(self, view):
        self.bindings.mode = static.modes.insert
        
        for event in self.viewEvents:
            self.view.disconnect(event)
        
        for event in self.docEvents:
            self.doc.disconnect(event)
    
    ########################
    ###   EVENT HANDLERS
    ########################
        
    def onKeyPress(self, view, event):
        """ initial key press processing """
        self.act.trace.keyPress(event)
        
        if self.extraMessageLife > 0:
            self.extraMessageLife -= 1
            
        self.setMessage()
        doPropogate = False
        currentMode = self.bindings.mode
        
        #call any rules set by modes
        for life, rule in self.rules:
            life -= 1
            if callable(rule):
                rule(self.act, event)
            if life == 0:
                self.rules.remove((1, rule))
        
        # Always return to command mode when Escape is pressed.
        if (event.keyval == gtk.keysyms.Escape):
            self.bindings.mode = static.modes.command
            doPropogate = True
            
        # directional keys in selection mode
        elif (currentMode == static.modes.selection and self.keyboard.isDirectionalPressed(self.act, event)):
            self.bindings.mode = static.modes.command
            doPropogate = False
            
        # Ignored keys.
        elif currentMode == static.modes.insert \
            or event.keyval in static.ignored_keys \
                and currentMode != static.modes.ex:
                doPropogate = False
                
        # Process keypress
        else:
            doPropogate = self.processKey(event)
        
        self.setMessage()
        return doPropogate
    
    def onButtonRelease(self, doc, view):
        """ if the user is in command mode and they select some text,
        then they enter either selection or visual mode, if they then deselect that text, then they re-enter command mode """
        currentMode = self.bindings.mode
        if opts.useSelectionMode:
            m = static.modes.selection
        else:
            m = static.modes.visual
            
        if currentMode in (static.modes.command, m):
            if self.doc.get_has_selection():
                self.bindings.mode = m
            else:
                self.bindings.mode = static.modes.command
    
    def processKey(self, event):
        """ second level of keypress processing
        
        if a binding doesn't exist for the event passed in
        
            if it's a number,
                it's added to ViBase.vigtk.number
            otherwise
                the current mode's handle() is called
                
        otherwise
            if the function isn't callable,
                key pressed is added to the stack
                
            otherwise
            
                determine where the cursor is
                
                if it's repeatable,
                
                    call function specified number of times (self.number)
                    reset numLines, number and stack
                    
                otherwise
                
                    call function
                    set numLines to number
                    reset number
                    
                    if the function is final,
                        reset numLines and stack
                        
                if the position is to be preserved,
                    move the cursor back to where it started at
        
        finally, if self.returnToMode is set to something,
            set that mode.
        """
        
        currentMode = self.bindings.mode
        control, meta = self.keyboard.modifiers(self.act, event)
        self.act.trace.info(1, "\t%s %s %s %s", currentMode, event.keyval, control, meta)
        
        bindingInfo = None
        doPropogate = currentMode != static.modes.insert
        keycombo = [currentMode, event.keyval, control, meta, "".join(self.stack)]
        #determine if there is a binding, and put it into bindingInfo
        if not self.bindings.vigm[currentMode].ignore(self, event):
            bindingInfo = self.vigtk.registry[(_ for _ in keycombo)]
        
        #if no binding, remove stack from keycombo and try again
        if not bindingInfo:
            keycombo[-1] = ""
            bindingInfo = self.vigtk.registry[(_ for _ in keycombo)]
            
            #make sure this binding doesn't want the stack to be part of the keycombo
            if bindingInfo and not bindingInfo['IgnoreStack']:
                bindingInfo = None
                
        if bindingInfo is None:
            self.act.trace.info(1, "\tthe binding -- %s : %s doesn't exist", currentMode, keycombo[1:])
            if event.keyval >= ord('0') and event.keyval <= ord('9'):
                #event is a number
                self.number.append(chr(event.keyval))
                self.act.trace.info(1, "\tself.number : %s", self.number)
            
            if event.keyval >= 65456 and event.keyval <= 65465:
                #keypad nums
                self.number.append(str(event.keyval-65456))
                self.act.trace.info(1, "\tself.number : %s", self.number)
            
            #make current mode handle the event
            self.act.trace.info(1, "\tmaking %s handle the event", currentMode)
            doPropogate = self.bindings.vigm[currentMode].handle(self.act, event)
        else:
            function        = bindingInfo["Function"]
            if function:
                self.act.trace.info(1, "\tCalling : %s", function.__name__)
            isFinal         = bindingInfo["Final"]
            isRepeatable    = bindingInfo["Repeatable"]
            afterMode       = bindingInfo["AfterMode"]
            preservePos     = bindingInfo["PreservePos"]
            recordAction    = bindingInfo["RecordAction"]
            pos = None
            
            if callable(function):
                def operation(act, preservePos, isRepeatable, isFinal, number, numLines, stack):
                    args = [act]
                    self.stack = stack
                    self.numLines = numLines
                    
                    if preservePos:
                        pos = self.cursor.getIter(self.act)
                        
                    act.trace.info(2, "\tfunction is callable")
                    if isRepeatable:
                        act.trace.info(2, "\tfunction is repeatable")
                        [function(*args) for _ in range(int("".join(number or ["1"])) or 1)]
                        
                        act.trace.info(2, "\tresetting numbers")
                        self.number = ['0']
                        self.numLines = 0
                        self.stack = []
                        
                    else:
                        function(*args)
                        self.numLines = int("".join(self.number or ["1"]))
                        self.number = []
                        
                        if isFinal:
                            self.act.trace.info(2, "\tfunction is final")
                            self.numLines = 0
                            self.stack = []
                    
                    if preservePos:
                        self.cursor.moveInsert(self.act, pos)
                
                number = list(self.number)
                numLines = self.numLines
                
                op = lambda act : operation(act, preservePos, isRepeatable, isFinal, number, numLines, self.stack)
                
                if recordAction:
                    #store lastOperation so keybindings can call it again if need be (i.e. . option in command mode)
                    self.lastOperation = op
                
                #call that operation
                op(self.act)
                    
            else:
                self.act.trace.info(2, "\tfunction is not callable")
                if function is None:
                    self.addToStack(event)
            
            if afterMode:
                self.bindings.mode = afterMode
            
        if self.returnToMode:
            self.bindings.mode = self.returnToMode
            self.returnToMode = None
        
        return doPropogate
    
    
            
        
    
