all:
	@echo "Please run 'make install'."

install:
	@echo "Installing ..."
	`pwd`/install

uninstall:
	@echo "LOL Z. Dude you mad?"

clean: uninstall
distclean: clean
realclean: clean

.PHONY: all install uninstall clean distclean realclean

