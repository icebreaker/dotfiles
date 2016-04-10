#!/bin/bash

MESSAGE=$(cat)

FROM=$(echo "${MESSAGE}" | grep ^"From: " | sed -e 's/^From: //g' | sed -e 's/"//g')

NAME=$(echo "${FROM}"  | cut -d '<' -f 1 | sed -e 's/ $//g')
NICKNAME=$(echo "${NAME}" | cut -d ' ' -f 1 | tr '[:upper:]' '[:lower:]')
EMAIL=$(echo "${FROM}" | cut -d '<' -f 2 | sed -e 's/>$//g')

if ! grep -q "${EMAIL}" $HOME/.mutt/aliases; then
	echo "alias $NICKNAME $NAME $EMAIL" >> $HOME/.mutt/aliases
fi

echo "${MESSAGE}"
