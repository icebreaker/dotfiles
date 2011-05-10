# -*- coding: utf-8 -*-

#  gui.py - holds stuff related to the gui
#
#  Copyright (C) 2006 - Trond Danielsen
#  Copyright (C) 2008, 2009 - Stephen Moore
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


from gobject import GObject

from ViGedit import static
from ViGedit.vi import VIG_Vibase
from ViGedit.bindings import registry

########################
###
###   STATUSBAR
###
########################

class VIG_StatusBar(object):
    def __init__(self, window):
        self.statusbar = window.get_statusbar()
        self.context_id = self.statusbar.get_context_id("VigeditStatusbar")

    def update(self, text=None):
        """Update statusbar"""
        self.statusbar.pop(self.context_id)
        if text is not None:
            self.statusbar.push(self.context_id, text)

########################
###
###   MENUS
###
########################

class VIG_Menus(object):
    """Used to conveniently refer to particular menu choices"""
    
    def __init__(self, window):
        self.window = window
        self.ui_manager = self.window.get_ui_manager()
        
        self.menubar           = self.window.get_children()[0].get_children()[0]
        self.menu_save         = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveMenu")
        self.menu_saveAs       = self.ui_manager.get_action("/MenuBar/FileMenu/FileSaveAsMenu")
        self.menu_searchNext   = self.ui_manager.get_action("/MenuBar/SearchMenu/SearchFindNextMenu")
        self.menu_searchPrev   = self.ui_manager.get_action("/MenuBar/SearchMenu/SearchFindPreviousMenu")
        self.menu_quit         = self.ui_manager.get_action("/MenuBar/FileMenu/FileQuitMenu")
        self.menu_fileClose    = self.ui_manager.get_action("/MenuBar/FileMenu/FileCloseMenu")
        self.menu_indentRight  = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Indent")
        self.menu_indentLeft   = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/Unindent")
        self.menu_joinLines    = self.ui_manager.get_action("/MenuBar/EditMenu/EditOps_5/JoinLines")
        self.menu_selectAll    = self.ui_manager.get_action("/MenuBar/EditMenu/EditSelectAllMenu")
        self.menu_paste        = self.ui_manager.get_action("/MenuBar/EditMenu/EditPasteMenu")
        self.menu_cut          = self.ui_manager.get_action("/MenuBar/EditMenu/EditCutMenu")
        self.menu_copy         = self.ui_manager.get_action("/MenuBar/EditMenu/EditCopyMenu")
        
    def __getitem__(self, menuType):
        """ returns a reference to the specified menu """
        return getattr(self, "menu_%s" % menuType, None)
        
########################
###
###   WINDOW
###
########################

class VIG_Window(GObject):
    """An instance of this is attached to every gedit window"""

    def __init__(self, window):
        self.window = window
        self.menus = VIG_Menus(window)
        self.statusbar = VIG_StatusBar(window)
        self.registry = registry
        
        for view in self.window.get_views():
            self.attachInfo(view)
        
        self.events = [
            self.window.connect("tab-added", self.onTabAdded),
            self.window.connect("active-tab-changed", self.onActiveTabChanged),
        ]
    
    def attachInfo(self, view):
        view.set_data("vigtk", self)
        view.set_data("mode", static.modes.command)
        
        newVIbase = VIG_Vibase(self, view)
        view.set_data("vibase", newVIbase)
        
        newVIbase.bindings.mode = static.modes.command
        newVIbase.update()
        
    def onActiveTabChanged(self, window, tab):
        currentView = tab.get_view()
        vib = currentView.get_data("vibase")
        if vib is not None:
            vib.update()

    def onTabAdded(self, window, tab):
        self.attachInfo(tab.get_view())

    def deactivate(self):
        self.statusbar.update(None)
        for view in self.window.get_views():
            vib = view.get_data("vibase")
            vib.deactivate(view)
            view.set_data("vibase", None)
            view.set_data("vigtk", None)
            view.set_data("mode", None)
        
        for event in self.events:
            self.window.disconnect(event)
        self.window = None

    def updateUI(self):
        tab = self.window.get_active_tab()
        if tab:
            view = tab.get_view()
        else:
            view = self.window.get_active_view()
        if view:
            vib = view.get_data("vibase")
            if vib:
                vib.update()
                
                
