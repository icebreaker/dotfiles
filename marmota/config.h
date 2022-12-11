#define BOLD_IS_BRIGHT TRUE
.icon_name = "launchpad",
.title = NULL,
.allow_change_title = TRUE,
.allow_context_menu = TRUE,
.allow_context_menu_fullscreen = TRUE,
.allow_context_menu_close = TRUE,
.allow_context_menu_scrollbar = TRUE,
.allow_context_menu_font_scale = TRUE,
.allow_fullscreen_toggle_shortcut = TRUE,
.allow_copy_paste_shortcut = FALSE,
.allow_hold_escape_shortcut = TRUE,
.allow_font_scale_shortcut = TRUE,
.login_shell = TRUE,
.shell = NULL,
.word_char_exceptions = NULL,
.allow_scrollbar = TRUE,
.show_scrollbar = FALSE,
.scrollback_lines = 8192,
.scroll_on_keystroke = TRUE,
.scroll_on_output = TRUE,
.cursor_blink_mode = VTE_CURSOR_BLINK_OFF,
.cursor_shape = VTE_CURSOR_SHAPE_BLOCK,
.mouse_autohide = TRUE,
.maximized = TRUE,
.borderless = TRUE,
.fullscreen = FALSE,
.centered = TRUE,
.font = "JetBrains Mono ExtraBold 17",
.font_scale = 1.0,
.font_scale_increment = 0.1,
.allow_link = TRUE,
.allow_hyperlink = TRUE,
.link_regex = "[A-Za-z]+://[\\-_.!~*a-zA-Z\\d;?:@&=+$,#%/]+",
.link_handler = "xdg-open",
.link_cursor_name = "pointer",
.bold_is_bright = BOLD_IS_BRIGHT,
.bold_color = NULL,
.cursor_background_color = "#8E8E8E",
.cursor_foreground_color = "#000000",
.foreground_color = "#A6A6A6",
.background_color = "#000000",
.highlight_foreground_color = "#000000",
.highlight_background_color = "#BCBCBC",
.background_image_color = { 0, 0, 0, 1 },
.background_image_overlay_color = { 0, 0, 0, 0.8 },
.background_image = NULL,
.background_image_position = { 0, 0 },
.background_image_scale = { 1, 1 },
.allow_background_image_scale = FALSE,
.allow_background_image_autoscale = FALSE,
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
