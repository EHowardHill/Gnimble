#!/bin/bash

# 59 -> Home (KEY_HOME = 102)
sudo setkeycodes 59 102

# 60 -> End (KEY_END = 107)
sudo setkeycodes 60 107

# 61 -> F5 (KEY_F5 = 63)
sudo setkeycodes 61 63

# 62 -> Disabled (KEY_RESERVED = 0)
sudo setkeycodes 62 0

# 63 -> Disabled (KEY_RESERVED = 0)
sudo setkeycodes 63 0

# 64 -> Brightness Down (KEY_BRIGHTNESSDOWN = 224)
sudo setkeycodes 64 224

# 65 -> Brightness Up (KEY_BRIGHTNESSUP = 225)
sudo setkeycodes 65 225

# 66 -> Disabled (KEY_RESERVED = 0)
sudo setkeycodes 66 0

# 67 -> Disabled (KEY_RESERVED = 0)
sudo setkeycodes 67 0

# 68 -> Disabled (KEY_RESERVED = 0)
sudo setkeycodes 68 0

matchbox-window-manager &
sleep 2
exec chromium --kiosk 127.0.0.1:5000
