#!/bin/bash

DIR=`pwd`
GREP='.grep'

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${GREP}" ]; then
		ARGS=$(cat "${DIR}/${GREP}" | tr '\n' ' ')
		grep ${@} -n -R ${ARGS} "${DIR}"
		exit 0
	fi

	DIR=`dirname "${DIR}"`
done

grep -n -R ${@}
