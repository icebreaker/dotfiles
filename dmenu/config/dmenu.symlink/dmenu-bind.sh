#!/bin/bash
exe=`dmenu_path | dmenu -nb '#000000' -nf '#d8d8d8' -sb '#d8d8d8' -sf '#000000'` && eval "exec $exe"
