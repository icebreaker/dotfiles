#!/bin/bash

DIR=`pwd`
TEMPLATE='.template'

function process_template()
{
	eval "echo \"$(cat $1)\""
}

if [ -n "$1" ]; then
	EXTENSION=$(basename "$1" | cut -d '.' -f 2)
	EXTENSION_UP=$(echo "$EXTENSION" | tr '[a-z]' '[A-Z]')

	FILENAME=$(basename "$1" ".${EXTENSION}")
	FILENAME_UP=$(echo "$FILENAME" | tr '[a-z]' '[A-Z]')

	if [ -n "$EXTENSION" ]; then
		TEMPLATE=".template.${EXTENSION}"
	fi
fi

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${TEMPLATE}" ]; then
		process_template "${DIR}/${TEMPLATE}"
		exit 0
	fi
	DIR=`dirname "${DIR}"`
done
