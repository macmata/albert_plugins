#!/usr/bin/env sh

if [ ! -e "$HOME/.local/share/albert/org.albert.extension.python/modules/" ]; then
	echo "error Albert folder not present"
	exit 0
fi

cp Egrep.py "$HOME"/.local/share/albert/org.albert.extension.python/modules/Egrep.py
cp Pinboard.py "$HOME"/.local/share/albert/org.albert.extension.python/modules/Pinboard.py

if [ ! -e "$HOME/notes" ]; then
	echo "creating note folder"
	mkdir "$HOME/notes"
fi

if [ ! -e "$HOME/.config/environment.d" ]; then
	echo "creating wayland export config file"
	mkdir "$HOME/.config/environment.d"
	touch "$HOME/.config/environment.d/export.conf"
fi

echo "all required folder are present"
echo "fill $HOME/.config/environment.d/export.conf and $HOME/notes/"

