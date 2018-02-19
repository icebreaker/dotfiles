#!/bin/bash

DIR=`pwd`
FILE='.exclude'

function read_pattern_from_file()
{
	cat "$1" | tr '\n' ',' | sed 's/,$//' | sed 's|/||g'
}

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${FILE}" ]; then
		PATTERN=$(read_pattern_from_file "${DIR}/${FILE}")
		EXCLUDE=$(eval "echo --exclude-dir={$PATTERN}")
		grep ${@} -I -n -R $EXCLUDE $DIR
		exit 0
	fi

	DIR=$(dirname "${DIR}")
done

grep -n -R ${@}
