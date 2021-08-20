//
// This is the default compile time configuration header.
//
// Sets the window icon name.
//
// This can the name of "any icon" defined by your GTK theme.
//
// For example: "launchpad"
//
// If NULL, the default window icon is used.
//
.icon_name = "launchpad",
//
// Sets default window title.
//
// If empty string (""), it will leave the window unnamed.
//
// If NULL, it defaults to the executable name as provided by argv[0].
//
.title = NULL,
//
// Whether or not to allow executed commands to change the default window title.
//
.allow_change_title = TRUE,
//
// Whether or not to allow the context menu.
//
.allow_context_menu = TRUE,
//
// Whether or not to display the fullscreen menu item in the context menu.
//
.allow_context_menu_fullscreen = TRUE,
//
// Whether or not to display the close menu item in the context menu.
//
.allow_context_menu_close = TRUE,
//
// Whether or not to display the scrollbar menu item in the context menu.
//
.allow_context_menu_scrollbar = TRUE,
//
// Whether or not to allow fullscreen toggling via Alt+Enter.
//
.allow_fullscreen_toggle_shortcut = TRUE,
//
// Whether or not to allow copy/paste via Ctrl+Shift+C and V.
//
.allow_copy_paste_shortcut = FALSE,
//
// Whether or not to allow exit via Escape after the "child process"
// has exited, when launched in hold mode.
//
.allow_hold_escape_shortcut = TRUE,
//
// Whether or not to spawn a "login shell".
//
// Ignored when the "-e" command line argument is used.
//
.login_shell = TRUE,
//
// Set shell to execute on launch when no arguments are given.
//
// If NULL, the shell is auto-detected, if auto-detection fails
// "/bin/sh" is used as fallback.
//
// The fallback can be configured at compile time:
//
// make FALLBACK_SHELL=/bin/sh
//
.shell = NULL,
//
// Set word char exceptions.
//
// If NULL, the default word char exceptions are used.
//
.word_char_exceptions = NULL,
//
// Whether or not to allow scroll bar.
//
.allow_scrollbar = TRUE,
//
// Whether or not to show scroll bar on launch.
//
.show_scrollbar = FALSE,
//
// Set scroll(back) limit in lines.
//
//  0 = disable scroll
// -1 = infinite scroll
// +1 = maximum scroll
//
.scrollback_lines = 8192,
//
// Whether or not to scroll on keystroke.
//
.scroll_on_keystroke = TRUE,
//
// Whether or not to scroll on output.
//
.scroll_on_output = TRUE,
//
// Whether or not to blink the cursor.
//
// VTE_CURSOR_BLINK_SYSTEM
// VTE_CURSOR_BLINK_ON
// VTE_CURSOR_BLINK_OFF
//
// See: https://developer.gnome.org/vte/unstable/VteTerminal.html
//
.cursor_blink_mode = VTE_CURSOR_BLINK_OFF,
//
// Shape of the cursor.
//
// VTE_CURSOR_SHAPE_BLOCK
// VTE_CURSOR_SHAPE_IBEAM
// VTE_CURSOR_SHAPE_UNDERLINE
//
// See: https://developer.gnome.org/vte/unstable/VteTerminal.html
//
.cursor_shape = VTE_CURSOR_SHAPE_BLOCK,
//
// Whether or not to auto hide the mouse when typing.
//
.mouse_autohide = TRUE,
//
// Whether or not to maximize the window on launch.
//
.maximized = TRUE,
//
// Whether or not to make the window borderless on launch.
//
.borderless = TRUE,
//
// Whether or not to make the window fullscreen on launch.
//
.fullscreen = FALSE,
//
// Whether or not to make the window centered on launch.
//
.centered = TRUE,
//
// Sets font family and size.
//
// Must be a pango compatible font description string.
//
// Example: "IBM Plex Mono weight=650 19"
//
// See: https://developer.gnome.org/pango/stable/pango-Fonts.html#pango-font-description-from-string
//
//.font = "IBM Plex Mono weight=650 18",
.font = "JetBrains Mono ExtraBold 18",
//
// Sets font scale.
//
.font_scale = 1.0,
//
// Whetver or not to enable link support.
//
// If this is set to false, it will disable both regular and hyperlink support.
//
.allow_link = TRUE,
//
// Whether or not to enable native hyperlink support.
//
// See: https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
//
.allow_hyperlink = TRUE,
//
// Regular expression used to match links.
//
.link_regex = "[A-Za-z]+://[\\-_.!~*a-zA-Z\\d;?:@&=+$,#%/]+",
//
// Regular link & hyperlink handler.
//
// If NULL, link and hyperlink support is disabled.
//
.link_handler = "xdg-open",
//
// Sets link cursor name for links matched by the link_regex.
//
// If NULL, the default cursor is used.
//
.link_cursor_name = "pointer",
//
// Whether or not "bold" should use bright colors.
//
#define BOLD_IS_BRIGHT TRUE
.bold_is_bright = BOLD_IS_BRIGHT,
//
// Sets Bold highlight color.
//
// If NULL, the default color is used.
//
.bold_color = NULL,
//
// Sets cursor background color.
//
// If NULL, the default color is used.
//
.cursor_background_color = "#8E8E8E",
//
// Sets cursor foreground color.
//
// If NULL, the default color is used.
//
.cursor_foreground_color = "#000000",
//
// Sets foreground color.
//
// If NULL, the color at index 7 from colors is used.
//
.foreground_color = "#A6A6A6",
//
// Sets background color.
//
// If NULL, the color at index 0 from colors is used.
//
.background_color = "#000000",
//
// Sets the foreground color for text which is highlighted.
//
// If NULL, it is unset. If neither highlight background nor highlight foreground are set,
// highlighted text (which is usually highlighted because it is selected) will be drawn with
// foreground and background colors reversed.
//
// See: https://developer.gnome.org/vte/unstable/VteTerminal.html#vte-terminal-set-color-highlight-foreground
//
.highlight_foreground_color = "#000000",
//
// Sets the background color for text which is highlighted.
//
// If NULL, it is unset. If neither highlight background nor highlight foreground are set,
// highlighted text (which is usually highlighted because it is selected) will be drawn with
// foreground and background colors reversed.
//
// See: https://developer.gnome.org/vte/unstable/VteTerminal.html#vte-terminal-set-color-highlight
//
.highlight_background_color = "#BCBCBC",
//
// Sets the initial 16 dark and bright colors.
//
// If more colors are needed or desired, this needs to be specified at compile time.
//
// make MAX_COLORS=24
//
// In the example above, we can now define 24 colors, instead of the default 16.
//
// Omitted entries will default to hard-coded values.
//
// See: https://developer.gnome.org/vte/unstable/VteTerminal.html#vte-terminal-set-colors
//
// Colors (including the various background and foreground) are parsed via `gdk_rgba_parse`.
//
// See: https://developer.gnome.org/gdk3/unstable/gdk3-RGBA-Colors.html#gdk-rgba-parse
//
.colors = {
	// Dark
	"rgb(0,0,0)",		// Black
	//"rgb(23,20,33)",	// Black
	"rgb(192,28,40)",	// Red
	"rgb(38,162,105)",	// Green
	"rgb(162,115,76)",	// Yellow
	"rgb(90,90,128)",	// Blue
	"rgb(128,71,128)",	// Magenta
	"rgb(42,161,179)",	// Cyan
	"rgb(166,166,166)", // White
#if BOLD_IS_BRIGHT
	// Dark
	"rgb(0,0,0)",		// Black
	//"rgb(23,20,33)",	// Black
	"rgb(192,28,40)",	// Red
	"rgb(38,162,105)",	// Green
	"rgb(162,115,76)",	// Yellow
	"rgb(90,90,128)",	// Blue
	"rgb(128,71,128)",	// Magenta
	"rgb(42,161,179)",	// Cyan
	"rgb(166,166,166)", // White
#else
	// Bright
	"rgb(94,92,100)",	// Black
	"rgb(246,97,81)",	// Red
	"rgb(51,218,122)",	// Green
	"rgb(233,173,12)",	// Yellow
	"rgb(42,123,222)",	// Blue
	"rgb(192,97,203)",	// Magenta
	"rgb(51,199,222)",	// Cyan
	"rgb(224,224,224)"	// White
#endif
}
