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


# Get the current IP address of the wlan0 interface (or your wifi interface)
IP_ADDRESS=$(ip -4 addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1)

# Robust IP check (handles multiple IPs or no IP)
if [[ -z "$IP_ADDRESS" ]]; then
    echo "Error: Could not determine IP address for wlan0. Check your wifi connection."
    exit 1
fi

# Generate the certificate using the obtained IP address
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365 \
    -subj "/C=US/ST=Texas/L=Longview/O=Gnimble/CN=$IP_ADDRESS"

echo "Certificate and key generated using IP: $IP_ADDRESS"

systemctl restart gnimble-server

echo "Flask server 'gnimble-server' restarted."