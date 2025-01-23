#!/bin/bash

if [ "$#" -eq 2 ]; then
    SSID="$1"
    PASSWORD="$2"
    nmcli dev wifi connect "$SSID" password "$PASSWORD"
else
    # If only SSID is passed, no password is assumed (open network)
    SSID="$1"
    nmcli dev wifi connect "$SSID"
fi