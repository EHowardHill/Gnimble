#!/usr/bin/env bash

set -e
SUDOERS_FILE="/etc/sudoers.d/connect_sh"

chmod 755 ./connect.sh

cat << EOF > "$SUDOERS_FILE"
# Allow everyone to run connect.sh without password
ALL ALL=(root) NOPASSWD: /home/user/wifi/connect.sh
EOF

chmod 440 "$SUDOERS_FILE"