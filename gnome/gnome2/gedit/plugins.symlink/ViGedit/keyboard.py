# -*- coding: utf-8 -*-

#  keyboard.py - handles stuff to do with the keyboard
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

import time

class VIG_Keyboard(object):
    """functions to do stuff with keyboard"""
    
    ########################
    ###   EMIT
    ########################
    
    def makeEvent(self, act, keyval, state=None):
        for keycode, group, level in act.gdk.keymap_get_default().get_entries_for_keyval(keyval):
            #just need to set keycode, group, level to one of the results from this function
            pass
        
        nextEvent = act.gdk.Event(act.gdk.KEY_PRESS)
        nextEvent.window = act.vigtk.window.window
        nextEvent.send_event = 1
        nextEvent.string = str(unichr(act.gdk.keyval_to_unicode(keyval)))
        nextEvent.time = int(time.time())
        
        if state:
            nextEvent.state = state
        else:
            nextEvent.state = act.gdk.MOD2_MASK
            
            if level == 1:
                nextEvent.state = nextEvent.state | act.gdk.SHIFT_MASK
        
        nextEvent.keyval = keyval
        nextEvent.hardware_keycode = keycode
        nextEvent.group = group
        
        return nextEvent

    def emitName(self, act, name, state=None):
        newEvent = self.makeEvent(act, getattr(act.gtk.keysyms, name), state)
        self.emitEvent(act, newEvent)
    
    def emitNames(self, act, *names):
        for name in names:
            self.emitName(act, name)

    def emitNumber(self, act, keyval, state=None):
        newEvent = self.makeEvent(act, keyval, state)
        self.emitEvent(act, newEvent)
    
    def emitEvent(self, act, event):
        keyName = act.gdk.keyval_name(event.keyval)
        
        try:
            action = {
                'left'      : act.pos.move_Backward,
                'right'     : act.pos.move_Forward,
                'up'        : act.pos.move_Up,
                'down'      : act.pos.move_Down,
                'end'       : act.pos.move_LineEnd,
                'home'      : act.pos.move_LineBegin,
                'page_down' : act.pos.move_PageDown,
                'page_up'   : act.pos.move_PageUp,
            }[keyName.lower()](act)
        except KeyError:
            act.vibase.view.emit("key-press-event", event)
    
    def emitNewLine(self, act):
        act.vibase.view.emit("insert-at-cursor", "\n")
    
    ########################
    ###   MODIFIERS
    ########################
    
    def modifiers(self, act, event):
        return self.isControlPressed(act, event), self.isAltPressed(act, event)
        
    def isControlPressed(self, act, event):
        ctrl = event.state & act.gdk.CONTROL_MASK
        if ctrl:
            return True
        else:
            # necessary if control has been pressed on it's own
            return event.keyval in (65507, 65508)

    def isAltPressed(self, act, event):
        alt = event.state & act.gdk.MOD1_MASK
        if alt:
            return True
        else:
            # necessary if control has been pressed on it's own
            return event.keyval in (65513, 65514)

    def isShiftPressed(self, act, event):
        return event.keyval in (65505, 65506)

    def isModifierPressed(self, act, event):
        return True in (
            self.isControlPressed(act, event),
            self.isAltPressed(act, event),
            self.isShiftPressed(act, event),
        )

    def isDirectionalPressed(self, act, event):
        return event.keyval in (
            act.gtk.keysyms.Up,
            act.gtk.keysyms.Down,
            act.gtk.keysyms.Left,
            act.gtk.keysyms.Right
        )
        

instance = VIG_Keyboard()
