#!/bin/bash

mkdir -p /mnt/usb
mount -o umask=0 /dev/sda1 /mnt/usb
mkdir -p /mnt/usb/raw