#!/bin/bash

# Connect to Wi-Fi (if SSID and password are provided)
if [ "$#" -eq 2 ]; then
    SSID="$1"
    PASSWORD="$2"
    nmcli dev wifi connect "$SSID" password "$PASSWORD"
elif [ "$#" -eq 1 ]; then  # Handle case where only SSID is provided
    SSID="$1"
    nmcli dev wifi connect "$SSID"
else
    echo "Usage: $0 <SSID> [<PASSWORD>]"  # Informative usage message
    exit 1
fi