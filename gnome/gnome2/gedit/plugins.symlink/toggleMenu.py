import gedit
import gtk
import os

# Toggle menu item XML
ui_manager_xml = """
<ui>
  <menubar name="MenuBar">
    <menu name="ViewMenu" action="View">
      <placeholder name="ViewOps_2">
        <separator/>
        <menuitem name="toggleMenuBar" action="toggleMenuBar"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class toggleMenuInstance:
  def __init__(self, plugin, window):
    
    self._window = window
    self._plugin = plugin
    
    # Find location of Toggle Menu config file (if it's possible)
    try: self._config     = os.path.expanduser('~')+"/.toggleMenu"
    except: self._config  = ""
    
    # Get gEdit main menu bar object
    self._manager     = self._window.get_ui_manager()
    self._menuBar     = self._manager.get_widget("/ui/MenuBar")
    self._menuVisible = True
    
    # Append custom menu item and key shortcut to toggle menu bar
    toggleMenuBar = (
      'toggleMenuBar',
      None,
      _("Toggle Menu"),
      '<Ctrl><Alt>M',
      _("Show or Hide Menu Bar"),
      self.toggle
    )
    self._action_group = gtk.ActionGroup("toggleMenuBar")
    self._action_group.add_actions([toggleMenuBar])
    self._manager.insert_action_group(self._action_group, -1)
    
    self._ui_id = self._manager.add_ui_from_string(ui_manager_xml)
    
    # Auto start with menu hidden?
    try:
      if os.path.exists(self._config):
        self._menuBar.hide()
        self._menuVisible = False
        
    except: pass
    
    # Track gedit window for sudden fullscreen movements
    self._trackWindow_id = self._window.connect("window-state-event", self.trackWindow)
    
  def trackWindow(self, window, callback_data):
    if not callback_data.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN and callback_data.changed_mask & gtk.gdk.WINDOW_STATE_FULLSCREEN:
      # If menu wasn't visible before fullscreen, hide it again (with fake toggle)
      if not self._menuVisible:
        self.toggle("_")
      
  
  # Show menu, remove custom menu item & keyboard shortcut
  def deactivate(self):
    self._menuBar.show()
    self._manager.remove_ui(self._ui_id)
    self._manager.ensure_update()
    
    self._window.disconnect(self._trackWindow_id)
    
    del self
  
  # Toggle menu bar and save current status in file (kinda)
  def toggle(self, action):
    if self._menuBar.flags() & gtk.VISIBLE:
      
      self._menuBar.hide()
      self._menuVisible = False
      
      try: open(self._config, 'w').close()
      except: pass
    
    else:
      
      self._menuBar.show()
      self._menuVisible = True
      
      try: os.unlink(self._config)
      except: pass

# Basic gedit plugin structure (nothing interesting)
class toggleMenuPlugin(gedit.Plugin):
  def __init__(self):
    gedit.Plugin.__init__(self)
    self._instances = {}
  
  def activate(self, window):
    self._instances[window] = toggleMenuInstance(self, window)
    
  def deactivate(self, window):
    self._instances[window].deactivate()
    del self._instances[window]
    
  def update_ui(self, window):
    pass
