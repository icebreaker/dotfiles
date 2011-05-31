My Dotfiles
===========
I've been sharing my `.dotfiles` for quite some time now, but it was more of a
chaotic mess than something really useful for another earthling.

Going on the `thematic` organization route with `symlinks` is a lot better for
a number of reasons which I'm not going to tackle in this very README.

Be Back After The Break
-----------------------
                   ,
                  / \,,_  .'|
               ,{{| /}}}}/_.'
              }}}}` '{{'  '.
            {{{{{    _   ;, \
         ,}}}}}}    /o`\  ` ;)
        {{{{{{   /           (
        }}}}}}   |            \
       {{{{{{{{   \            \          ,-------------------------------.
       }}}}}}}}}   '.__      _  |        /       HI                        \
       {{{{{{{{       /`._  (_\ /       /      /   \                        |
        }}}}}}'      |    //___/   --= <   VVVI     HI-HI-HI                |
    jgs `{{{{`       |     '--'         \                   \               |
         }}}`                            \                  HIM-HIM-HIM!!!  /
                                          '--------------------------------'

Getting Started
---------------
* `git clone git://github.com/icebreaker/dotfiles ~/.dotfiles`
* `cd ~/.dotfiles`
* `make install` (or if you don't have `make`, then `./install`)

If you `clone` to a non-standard location a.k.a not `$HOME/.dotfiles` be sure
to edit `bash/bashrc.symlink` and update the `DOTFILES` variable.

Behind the scenes magic
-----------------------
First of all your `.dotfiles` directory is scanned and all files ending with `.bsh`
extension are `sourced` whenever you open up a terminal; this means that you can
break down your `EXPORTS`, `ENV` at your hearts content without stuffing everything
in a single file by just *simply* dropping in a *new file* somewhere within `.dotfiles`
and `presto` you don't even need to edit anything. Neat isn't it?

Secondly, whenever you execute `make install` your `.dotfiles` directory is scanned for 
files ending with `.symlink`.

Some real life examples in order to illustrate how this works:

* `$DOTFILES`/vim/vimrc.symlink => `$HOME`/.vimrc
* `$DOTFILES`/vim/vim.symlink => `$HOME`/.vim
* `$DOTFILES`/gnome/gnome2/gedit/themes.symlink => `$HOME`/.gnome2/gedit/themes

That's all folks. Simple huh? 

A small price to pay for well a organized `.dotfiles` collection which makes updating a joy and breeze.

Scripts
-------
In the `$DOTFILES/bin` directory (which is automatically added to the PATH) there are
a couple of `helper` or `wrapper` scripts which make my life easier in the first place
and they might do the same for yours.

I would like to highlight the `dot-aliases` script which will list all your registered aliases
sorted by topic inside your `.dotfiles` directory. You can even filter by topic using `dot-aliases mytopic`.

Also the `dot-update` will update your `.dotfiles` regardless of your current directory and it will also
automatically reload your `.bashrc`.

TODO
----
- use [pathogen](git://github.com/tpope/vim-pathogen.git) and git submodules for Vim
	- CSApprox as submodule
	- Solarized as submodule
	- ScrollColor as submodule

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
