.DotFiles
=========
I've been sharing my `.dotfiles` for quite some time now, but it was more of a
chaotic mess than something really useful for another earthling.

Going on the `thematic` organization route with `symlinks` is a lot better for
a number of reasons which I'm not going to tackle in this very README.

**In six words**: My `.dotfiles` never been so **happy**!

Getting Started
---------------
* `git clone git://github.com/icebreaker/dotfiles ~/.dotfiles`
* `cd ~/.dotfiles`
* `./p0wn` (*installs symlinks to $HOME - files and directories alike*)

If you `clone` to a non-standard location a.k.a not `$HOME/.dotfiles` be sure
to edit `p0wn` and `bash/bashrc.symlink` then update the `$DOTFILES` variable
accordingly, but this rather Non-Orthodox practice is highly discouraged by the 
high-priests of `The Dotfile Temple`. Earthlings, you have been **WARNED**.

Behind the scenes magic
-----------------------
First of all your `.dotfiles` directory is scanned and all files ending with `.bsh`
extension are `sourced` whenever you open up a terminal; this means that you can
break down your `EXPORTS`, `ENV` at your hearts content without stuffing everything
in a single file by just *simply* dropping in a *new file* somewhere within `.dotfiles`
and `presto` you don't even need to edit anything. Neat isn't it?

Secondly, whenever you execute `./p0wn` your `.dotfiles` directory is scanned for 
files ending with `.symlink`; this support two types of symlinks:

* $HOME/.yoursymlink
* $HOME/.yourconfig/yoursymlink (the target directory is created if doesn't exist)

Now let's see with some real life examples how this works (source => target):

* $DOTFILES/vim/vimrc.symlink => $HOME/.vimrc
* $DOTFILES/vim/vim.symlink => $HOME/.vim
* $DOTFILES/gnome/gnome2/gedit/themes.symlink => $HOME/.gnome2/gedit/themes

That's all folks. Simple huh? A small price to pay for well a organized `.dotfiles`
collection which makes updating a joy and breeze.

Contribute
----------
* Fork the project.
* Make your feature addition or bug fix.
* Send me a pull request. Bonus points for topic branches.

License
-------
Copyright (c) 2011, Mihail Szabolcs

Everything is provided **as-is** under the **MIT** license. For more information,
see *LICENSE*.
