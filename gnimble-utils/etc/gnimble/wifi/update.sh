#!/bin/bash

# Additional packages
apt update -y

# Maintenance
apt upgrade -y
apt --fix-broken install -y
apt autoremove -y