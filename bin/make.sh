#!/bin/bash

DIR=`pwd`
PROJECT='.project'

while test "${DIR}" != "/"; do
	if [ -f "${DIR}/${PROJECT}" ]; then
		echo "Trying to build in ${DIR} ..."
		make -C "${DIR}" -f "${PROJECT}" $@
		exit
	fi
	DIR=`dirname "${DIR}"`
done

echo "No ${PROJECT} found!" > /dev/stderr
