#!/bin/sh

# Copyright (C) 2017-2018 Vilniaus Blokas UAB, https://blokas.io/pisound
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.
#

find_pd_object()
{
	PATCH_DIR=$(dirname "$2")
	grep -qr -m1 --include \*.pd "$1" "$PATCH_DIR"
}

if [ "$2" != '--summary' ]; then
	# Determine if MIDI keyboard should be enabled.
	if find_pd_object "notein" "$1" || find_pd_object "r notes" "$1"; then
		echo "midi_keyboard: On"
	fi

	PATCH_DIR=$(dirname "$1")

	# Determine if MEC controls are defined.
	if [ $(ls -1 "$PATCH_DIR"/*-module.json 2>/dev/null | wc -l) != 0 ]; then
		echo "mec_controls: On"
	fi
fi

if echo "$1" | grep -q "blokas.yml\$"; then
	# Echo the entire file with all the filled information.
	cat "$1"
else
	# Generate json with only the information we know on the 'legacy' patches.
	PATCH_DIR=`dirname "$1"`
	DIR_NAME=`basename "$PATCH_DIR"`
	#JSON='{"name":"'$DIR_NAME'","entry":"main.pd"}'
	#echo $JSON
	echo "name: \"$DIR_NAME\""
	echo "entry: \"main.pd\""
fi
