#!/bin/sh

# Copyright (C) 2017-2018 Vilniaus Blokas UAB, https://blokas.io/pisound
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.
#

. /usr/local/pisound/scripts/common/common.sh
flash_leds 100

#!/bin/bash
#amixer cset numid=11 off

systemctl stop eyesy-python.service
systemctl stop eyesy-web.service
systemctl stop eyesy-web-socket.service
systemctl stop eyesy-pd.service