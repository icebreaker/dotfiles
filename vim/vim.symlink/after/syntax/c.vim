" highlight foreach
syn keyword Function foreach

" highlight all types that end with _t or _s (i.e type_t, or foo_s)
syn match Type /\<\i\+_t\>/
syn match Type /\<\i\+_s\>/

" highlight all uppercase "constants" or "macros"
syn match PreProc /\zs\<[A-Z_][A-Z0-9_]\+\>/

" highlight some lua, gtk, gdk, glib, pango and vte types
syn match Type /\<luaL_.\{-}\>/
syn match Type /\<lua_.\{-}\>/
syn match Type /\<Gdk.\{-}\>/
syn match Type /\<Gtk.\{-}\>/
syn match Type /\<Vte.\{-}\>/
syn match Type /\<Pango.\{-}\>/
syn match PreProc /\<GDK_.\{-}\>/
syn match Function /\<vte_.\{-}\>/
syn match Function /\<gtk_.\{-}\>/
syn match Function /\<gdk_.\{-}\>/
syn match Function /\<g_.\{-}\>/
syn match Function /\<pango_.\{-}\>/
syn keyword Type GPid GError
syn keyword Type gpointer gpointer gboolean gint guint gfloat gdouble gchar guchar glong gulong gshort gushort gsize

syn match Function /\<oln_.\{-}\>/

" vim:set sw=2:
