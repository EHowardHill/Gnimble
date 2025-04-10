#!/bin/bash

# Check the number of arguments and attempt Wi-Fi connection
if [ "$#" -eq 2 ]; then
    SSID="$1"
    PASSWORD="$2"
    # Attempt to connect with SSID and password
    nmcli dev wifi connect "$SSID" password "$PASSWORD"
    STATUS=$?  # Capture the exit status of nmcli
elif [ "$#" -eq 1 ]; then
    SSID="$1"
    # Attempt to connect with SSID only (no password)
    nmcli dev wifi connect "$SSID"
    STATUS=$?  # Capture the exit status of nmcli
else
    echo "Usage: $0 <SSID> [<PASSWORD>]"  # Informative usage message
    exit 1
fi