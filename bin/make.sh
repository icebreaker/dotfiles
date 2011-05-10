#!/bin/sh

EHOME=`echo $HOME | sed "s/#/\#/"`
DIR=`pwd`

while test "$DIR" != "/"; do
	for m in .project; do
		if [ -f "${DIR}/${m}" ]; then
			cd "${DIR}"
			make $@
			exit
		fi
	done
	DIR=`dirname "${DIR}"`
done

echo "No project found!" > /dev/stderr
