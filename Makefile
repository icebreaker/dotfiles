all:
	@echo "Please run 'make install'."

update:
	`pwd`/update

install:
	`pwd`/install

uninstall:
	@echo "LOL Z. Dude you mad?"

clean: uninstall
distclean: clean
realclean: clean

.PHONY: all update install uninstall clean distclean realclean

