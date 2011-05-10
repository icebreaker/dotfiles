# -*- coding: utf-8 -*-

#  cursor.py - processing for the cursor
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

class VIG_Cursor(object):
    """functions to control the cursor with"""
        
    def getIter(self, act):
        return act.vibase.doc.get_iter_at_mark(act.vibase.doc.get_insert())
        
    def moveInsert(self, act, newIter, select=False):
        mark = act.vibase.doc.get_insert()
        
        if select:
            act.vibase.doc.move_mark(mark, newIter)
        else:
            act.vibase.doc.place_cursor(newIter)
         
        act.vibase.view.scroll_to_mark(mark, 0.0)
        
    def goToLine(self, act, line):
        cursor = self.getIter(act)
        cursor.set_line(line - 1)
        self.moveInsert(act, cursor)
    
    def move(self, act, directionType, num):
        act.vibase.view.emit("move-cursor", directionType, num, act.vibase.select)
        
    def toEmptyLine(self, act, forward = True):
        act.pos.move_LineBegin(act)
        cursor = self.getIter(act)
        if forward:
            direction = "forward"
        else:
            direction = "backward"
            
        while True:
            getattr(cursor, "%s_visible_line" % direction)()
            print "line %d : %d chars, start: %s, end : %s" % (cursor.get_line(), cursor.get_chars_in_line(), cursor.ends_line(), cursor.starts_line())
            if cursor.get_chars_in_line() == 1:
                if cursor.ends_line() and cursor.starts_line():
                    self.moveInsert(act, cursor)
                    break
            
            if cursor.is_start() or cursor.is_end():
                act.trace.info(2, "reached boundary of document")
                break
    
########################
###
###   MOVING
###
########################

    ########################
    ###   DIRECTION
    ########################
    
    def move_Up_Lines(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, -num)
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, -num)
        
    def move_Down_Lines(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, num)
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, num)
        
    def move_Up(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, -num)
        
    def move_Down(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_DISPLAY_LINES, num)
        
    def move_Forward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_VISUAL_POSITIONS, num)
        
    def move_Backward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_VISUAL_POSITIONS, -num)
       
    ########################
    ###   PAGE
    ########################
        
    def move_PageUp(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PAGES, -num)
        
    def move_PageDown(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PAGES, num)
        
    ########################
    ###   WORD
    ########################
        
    def move_WordForward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_WORDS, num)
       
    def move_WordBackward(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_WORDS, -num)
    
    ########################
    ###   BUFFER
    ########################
        
    def move_BufferTop(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_BUFFER_ENDS, -num)
        
    def move_BufferEnd(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_BUFFER_ENDS, num)
    
    ########################
    ###   LINE
    ########################
        
    def move_LineEnd(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, num)
        
    def move_LineBegin(self, act, num=1):
        self.move(act, act.gtk.MOVEMENT_PARAGRAPH_ENDS, -num)
    
    ########################
    ###   OTHER
    ########################
        
    def move_to_matching_bracket(self, act, num=1):
        prevMode = act.bindings.mode
        
        # get chars either side of the cursor
        # If either is a bracket, then we will search for the matching bracket
            
        cursor = self.getIter(act)
        for side in self.char_either_side(act, cursor):
            if side in ('(', ')'):
                opposite, newCursor = self.iter_for_bracket(act, side)
                self.moveInsert(act, newCursor)
                
                if opposite not in self.char_either_side(act, newCursor):
                    # no opposite found, reset cursor
                    self.moveInsert(act, cursor)
                
                act.bindings.mode = prevMode
                    
                return
            else:
                # Cursor isn't on a bracket, so let's look for some
                # First look to the left and the right for brackets
                # If we find brackets on both sides, then move to the closest one
                positions = []
                for side in  ('(', ')'):
                    opposite, newCursor = self.iter_for_bracket(act, side)
                    self.moveInsert(act, newCursor)
                    if opposite in self.char_either_side(act, newCursor):
                        positions.append(self.getIter(act))
                
                if len(positions) != 2:
                    # Didn't find brackets on both sides, reset cursor
                    self.moveInsert(act, cursor)
                else:
                    # Did find brackets on both sides, determine which is closer
                    distance1 = self.distance_between_iters(act, positions[0], cursor)
                    distance2 = self.distance_between_iters(act, positions[1], cursor)
                    if distance1 > distance2:
                        self.moveInsert(act, positions[1])
                    else:
                        self.moveInsert(act, positions[0])
        
        act.bindings.mode = prevMode
    
    def distance_between_iters(self, act, curs1, curs2):
        line1 = curs1.get_line()
        line2 = curs2.get_line()
        
        if line1 == line2:
            offset1 = curs1.get_line_offset()
            offset2 = curs2.get_line_offset()
            return abs(offset1 - offset2)
        else:
            if line1 > line2:
                # swap so line1 is above line2
                line1, line2 = line2, line1
            
            return abs(len(curs1.get_text(curs2)))
    
    def iter_for_bracket(self, act, side):
        def info(side):
            if side == '(':
                return ['parenleft', 'parenright', ')', 'f']
            else:
                return ['parenright', 'parenleft', '(', 'b']
            
        name, oppositeName, opposite, searchDirection = info(side)
        act.bindings.mode = act.modes.t, ["find", 1, searchDirection, name]
        act.keyboard.emitName(act, oppositeName)
        return opposite, self.getIter(act)
        
    def char_either_side(self, act, cursor):
        for direction in ('forward', 'backward'):
            side = self.getIter(act)
            getattr(side, '%s_char' % direction)()
            yield cursor.get_text(side)

    def buffer_word_boundary(self, buf):
        """get range for word under cursor"""
        iter = buf.get_iter_at_mark(buf.get_insert())
        start = iter.copy()

        if not iter.starts_word() and (iter.inside_word() or iter.ends_word()):
                start.backward_word_start()

        if not iter.ends_word() and iter.inside_word():
                iter.forward_word_end()

        return (start, iter)

    def get_word_under_cursor(self, act):
        doc = act.vibase.doc
        start, end = self.buffer_word_boundary(doc)
        return doc.get_text(start, end)

instance = VIG_Cursor()
        
