# mp.py - HTML preview of Markdown formatted text in Gedit using WebKit and the
# GitHub cascading stylesheet.
#
# Copyright (C) 2005 - Michele Campeotto
# Copyright (C) 2010 - Mihail Szabolcs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import gedit

import sys
import gtk
import webkit
import markdown

# Source: http://fgnass.posterous.com/github-markdown-preview
HTML_TEMPLATE = """<html><head><style type="text/css">
 .github {margin-left:auto;margin-right:auto;padding:0.7em;border:1px solid #E9E9E9;background-color:#f8f8f8;font-size:13.34px;font-family:helvetica,arial,freesans,clean,sans-serif;width:920px;}
 .github h1,h2,h3,h4,h5,h6{border:0;}
 .github h1{font-size:170%%;border-top:4px solid #aaa;padding-top:.5em;margin-top:1.5em;}
 .github h1:first-child{margin-top:0;padding-top:.25em;border-top:none;}
 .github h2{font-size:150%%;margin-top:1.5em;border-top:4px solid #e0e0e0;padding-top:.5em;}
 .github h3{margin-top:1em;}
 .github p{margin:1em 0;line-height:1.5em;}
 .github ul{margin:1em 0 1em 2em;}
 .github ol{margin:1em 0 1em 2em;}
 .github ul li{margin-top:.5em;margin-bottom:.5em;}
 .github ul ul,ul ol,ol ol,ol ul,{margin-top:0;margin-bottom:0;}
 .github blockquote{margin:1em 0;border-left:5px solid #ddd;padding-left:.6em;color:#555;}
 .github dt{font-weight:bold;margin-left:1em;}
 .github dd{margin-left:2em;margin-bottom:1em;}
 .github table{margin:1em 0;}
 .github table th{border-bottom:1px solid #bbb;padding:.2em 1em;}
 .github table td{border-bottom:1px solid #ddd;padding:.2em 1em;}
 .github pre{margin:1em 0;font-size:12px;background-color:#f8f8ff;border:1px solid #dedede;padding:.5em;line-height:1.5em;color:#444;overflow:auto;}
 .github pre code{padding:0;font-size:12px;background-color:#f8f8ff;border:none;}
 .github code{font-size:12px;background-color:#f8f8ff;color:#444;padding:0 .2em;border:1px solid #dedede;}
 .github a{color:#4183c4;text-decoration:none;}
 .github a:hover{text-decoration:underline;}
 .github a code,a:link code,a:visited code{color:#4183c4;}
 .github img{max-width:100%%;}
</style></head><body><div class="github">%s</div></body></html>"""

UI = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="MP" action="MP"/>
      </placeholder>
    </menu>
  </menubar>
</ui>"""

class MarkdownPreviewPlugin(gedit.Plugin):

	def __init__(self):
		gedit.Plugin.__init__(self)
			
	def activate(self, window):
		
		wndata = dict()
		window.set_data("MPData", wndata)

		sw = gtk.ScrolledWindow()
		sw.set_property("hscrollbar-policy",gtk.POLICY_AUTOMATIC)
		sw.set_property("vscrollbar-policy",gtk.POLICY_AUTOMATIC)
		sw.set_property("shadow-type",gtk.SHADOW_IN)

		wv = webkit.WebView() 				
		sw.add(wv)
		sw.show_all()
		
		panel = window.get_bottom_panel()
		
		image = gtk.Image()
		image.set_from_icon_name("gnome-mime-text-html", gtk.ICON_SIZE_MENU)
		panel.add_item(sw, "Markdown Preview", image)
		
		wndata["sw"] = sw
		wndata["wv"] = wv

		action = ("MP",
			  	None,
			  	"Markdown Preview",
			  	"<Control><Shift>G",
			  	"Updates the Markdown HTML preview.",
			  	lambda x, y: self.update_preview(y))
		
		wndata["ag"] = gtk.ActionGroup("MPActions")
		wndata["ag"].add_actions([action], window)

		manager = window.get_ui_manager()
		manager.insert_action_group(wndata["ag"], -1)

		wndata["ui_id"] = manager.add_ui_from_string(UI)
		
		manager.ensure_update()
	
	def deactivate(self, window):
		wndata = window.get_data("MPData")

		manager = window.get_ui_manager()
		manager.remove_ui(wndata["ui_id"])
		manager.remove_action_group(wndata["ag"])
		
		panel = window.get_bottom_panel()
		panel.remove_item(wndata["sw"])
		
		manager.ensure_update()
	
	def update_preview(self, window):
		wndata = window.get_data("MPData")
		
		view = window.get_active_view()
		if not view:
			 return
		
		doc = view.get_buffer()
		
		start = doc.get_start_iter()
		end = doc.get_end_iter()
		
		if doc.get_selection_bounds():
			start = doc.get_iter_at_mark(doc.get_insert())
			end = doc.get_iter_at_mark(doc.get_selection_bound())
		
		text = doc.get_text(start, end)
		html = HTML_TEMPLATE % (markdown.markdown(text),)
		
		wndata["wv"].load_string(html,'text/html','iso-8859-15','about:blank')

		bottom = window.get_bottom_panel()
		bottom.activate_item(wndata['sw'])
		bottom.set_property('visible',True)
