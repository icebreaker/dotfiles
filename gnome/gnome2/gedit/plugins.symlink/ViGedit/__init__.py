# -*- coding: utf-8 -*-

#  __init__.py - initialise the plugin
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

import gedit
from vigtk import VIG_Window

class VigeditPlugin(gedit.Plugin):
    """ Creates the VigeditWindowHelper on activate. """

    def activate(self, window):
        vigtk = VIG_Window(window)
        window.set_data("vigedit", vigtk)

    def deactivate(self, window):
        window.get_data("vigedit").deactivate()
        window.set_data("vigedit", None)
        
    def update_ui(self, window):
        window.get_data("vigedit").updateUI()
        
