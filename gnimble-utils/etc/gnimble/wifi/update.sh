#!/bin/bash

# Additional packages
apt update -y
apt install -y cups-client python3-pyudev

# Maintenance
apt upgrade -y
apt --fix-broken install -y
apt autoremove -y