# -*- coding: utf-8 -*-
#
# Auto Tab for gedit, automatically detect tab preferences for source files.
# Can be used together with the Modelines plugin without ill effect, modelines
# will take precedence.
#
# Copyright (C) 2007 Kristoffer Lundén (kristoffer.lunden@gmail.com)
# Copyright (C) 2007 Lars Uebernickel (larsuebernickel@gmx.de)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gedit
import gconf
import operator

class AutoTab(gedit.Plugin):

  def activate(self, window):
  
    self.window = window
    self.spaces_instead_of_tabs = False
    self.tabs_width = 2
    
    # Prime the statusbar
    self.statusbar = window.get_statusbar()
    self.context_id = self.statusbar.get_context_id("AutoTab")
    self.message_id = None

    # Init defaults, set up callbacks to get notified of changes
    client = gconf.client_get_default() 
    self.new_tabs_size(client)
    self.new_insert_spaces(client)
    client.notify_add("/apps/gedit-2/preferences/editor/tabs/tabs_size", self.new_tabs_size)
    client.notify_add("/apps/gedit-2/preferences/editor/tabs/insert_spaces", self.new_insert_spaces)

    for view in window.get_views(): 
      self.connect_handlers(view)
      self.auto_tab(view.get_buffer(), None, view)

    tab_added_id = window.connect("tab_added", lambda w, t: self.connect_handlers(t.get_view()))
    window.set_data("AutoTabPluginHandlerId", tab_added_id)

  def deactivate(self, window):
    tab_added_id = window.get_data("AutoTabPluginHandlerId")
    window.disconnect(tab_added_id)
    window.set_data("AutoTabPluginHandlerId", None)

    for view in window.get_views():
      self.disconnect_handlers(view)

    if self.message_id:
      self.statusbar.remove_message(self.context_id, self.message_id)

  def connect_handlers(self, view):
    doc = view.get_buffer()
    # Using connect_after() because we want other plugins to do their
    # thing first.
    loaded_id = doc.connect_after("loaded", self.auto_tab, view)
    saved_id  = doc.connect_after("saved", self.auto_tab, view)
    doc.set_data("AutoTabPluginHandlerIds", (loaded_id, saved_id))

  def disconnect_handlers(self, view):
    doc = view.get_buffer()
    loaded_id, saved_id = doc.get_data("AutoTabPluginHandlerIds")
    doc.disconnect(loaded_id)
    doc.disconnect(saved_id)
    doc.set_data("AutoTabPluginHandlerIds", None)
  
  # If default tab size changes
  def new_tabs_size(self, client, id=None, entry=None, data=None):
    self.tabs_width = client.get_int("/apps/gedit-2/preferences/editor/tabs/tabs_size")
    self.update_tabs(self.tabs_width, self.spaces_instead_of_tabs)
  
  # If default space/tabs changes
  def new_insert_spaces(self, client, id=None, entry=None, data=None):
    self.spaces_instead_of_tabs = client.get_bool("/apps/gedit-2/preferences/editor/tabs/insert_spaces")
    self.update_tabs(self.tabs_width, self.spaces_instead_of_tabs)

  # Update the values and set a new statusbar message  
  def update_tabs(self, size, space):
    view = self.window.get_active_view()
    if view:
      view.set_tab_width(size)
      view.set_insert_spaces_instead_of_tabs(space)
      self.update_status()
      
  # Statusbar message
  def update_status(self):
    view = self.window.get_active_view()
    if view:
      space = view.get_insert_spaces_instead_of_tabs()
      size = view.get_tab_width()
      if space:
        message = "%i Spaces" % size
      else:
        message = "Tabs"
      if self.message_id:
        self.statusbar.remove_message(self.context_id, self.message_id)
      self.message_id = self.statusbar.push(self.context_id, "Indentation: %s" % message)

  # Make sure correct tabs are displayed
  def update_ui(self, window):
    self.update_status()

  # These should be read out of gconf
  def set_sensible_defaults(self, language):
      language = language.lower()
      # This can and should be made more configurable
      if language == "python":
          self.update_tabs(4, True)
      elif language == "ruby":
          self.update_tabs(2, True)
      elif language == "php":
          self.update_tabs(4, False)

  # Main workhorse, identify what tabs we should use and use them.
  def auto_tab(self, doc, error, view):
    if error is not None:
      pass
    
    # Other plugins compatibility, other plugins can do
    # view.set_data("AutoTabSkip", True)
    # and Auto Tab will skip that document as long as this value is true.
    if view.get_data("AutoTabSkip"):
      self.update_status()
      return
    
    # Modelines plugin compatibility, if ModelineOptions has been set with
    # any tab related data, we assume Modelines has done the right thing and
    # just update our UI with the existing settings.
    modeline = view.get_data("ModelineOptions")
    if modeline:
      if modeline.has_key("tabs-width") or modeline.has_key("use-tabs"):
        self.update_status()
        return
		
		# End of Modelines stuff,
		# start of Auto Tabs own stuff

   		    
    start, end = doc.get_bounds()
    if not end:
      return
    text = doc.get_text(start, end)

    indent_count = {'tabs':0, 2:0, 3:0, 4:0, 8:0}
    last_indent = 0
    for line in text.splitlines():
      if len(line) == 0 or not line[0].isspace():
        continue
      
      if line[0] == '\t':
        indent_count['tabs'] += 1
        continue
        
      indent = 0
      while line.startswith(' '):
        indent += 1
        line = line[1:]
       
      if indent == last_indent:
        continue
      for i in (2, 3, 4, 8):
        if last_indent + i == indent:
          indent_count[i] += 1;
          break
      last_indent = indent

    # no indentations, leave old values
    if sum(indent_count.values()) == 0:
      # Use the filetype as the rule after everything else has been tried 
      language = doc.get_language()
      if language:
      # The docs say say something about this being the localized name. Could
      # be a problem?
        language = language.get_name()
        self.set_sensible_defaults(language)
      return

    winner = max(indent_count, key=indent_count.get)
    if winner == 'tabs':
      self.update_tabs(self.tabs_width, False)
    else:
      self.update_tabs(winner, True)
    
