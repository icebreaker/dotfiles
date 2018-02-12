#!/bin/bash

DIR=$(pwd)
TEMPLATE='.template'

function process_template()
{
	eval "echo \"$(cat $1)\""
}

function extract_filepath()
{
	local FILEPATH=""
	local SRCFOUND=0

	for s in $(dirname $1 | tr '/' '\n'); do
		if [ $SRCFOUND -eq 1 ]; then
			if [ -z "$FILEPATH" ]; then
				FILEPATH=$s
			else
				FILEPATH="$FILEPATH/$s"
			fi
		elif [ "$s" == "src" ]; then
			SRCFOUND=1
		fi
	done

	echo $FILEPATH
}

if [ -n "$1" ]; then
	EXTENSION=$(basename "$1" | cut -d '.' -f 2)
	EXTENSION_UP=$(echo "$EXTENSION" | tr '[a-z]' '[A-Z]')

	FILENAME=$(basename "$1" ".${EXTENSION}")
	FILENAME_UP=$(echo "$FILENAME" | tr '[a-z]' '[A-Z]')

	FILEPATH=$(extract_filepath "$1")

	if [ -n "$EXTENSION" ]; then
		TEMPLATE=".template.${EXTENSION}"
	fi
fi

while [ "$DIR" != "/" ]; do
	if [ -f "$DIR/$TEMPLATE" ]; then
		process_template "$DIR/$TEMPLATE"
		exit 0
	fi
	DIR=$(dirname "$DIR")
done
