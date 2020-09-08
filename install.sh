#!/bin/bash

if [ "$HOME" == "/home/codespace" ]; then
	mv ~/.bashrc ~/.codespacesrc
	mv ~/dotfiles ~/.dotfiles
	~/.dotfiles/bin/dot-install
	source ~/.bashrc
else
	echo "This install script is for codespaces only! Please run bin/dot-install"
fi
