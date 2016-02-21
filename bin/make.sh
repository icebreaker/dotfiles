#!/bin/bash

DIR=`pwd`
PROJECT='.project'

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${PROJECT}" ]; then
		make -C "${DIR}" -f "${PROJECT}" $@
		exit 0
	fi
	DIR=`dirname "${DIR}"`
done

echo "No ${PROJECT} found!" > /dev/stderr
exit 0
