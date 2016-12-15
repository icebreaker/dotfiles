#!/bin/bash

DIR=`pwd`
EXCLUDE='.exclude'

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${EXCLUDE}" ]; then
		filter --exclude-from "${DIR}/${EXCLUDE}"
		exit 0
	fi

	DIR=`dirname "${DIR}"`
done

cat
