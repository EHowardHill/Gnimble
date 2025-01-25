#!/bin/bash

apt update -y
apt upgrade -y
apt --fix-broken install -y
apt autoremove -y