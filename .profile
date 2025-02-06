#!/bin/bash

#
# 1. Remap certain function keys with xmodmap
#
xmodmap -e "keycode 67 = XF86Back"      # F1 -> Back
xmodmap -e "keycode 68 = XF86Forward"   # F2 -> Forward
xmodmap -e "keycode 69 = XF86Refresh"   # F3 -> Refresh
# ...
# Confirm these codes for your actual F8, F9, F10, F11:
xmodmap -e "keycode 73 = Home"          # F7 or F8
xmodmap -e "keycode 74 = Prior"         # F8 or F9
xmodmap -e "keycode 75 = Next"          # F9 or F10
xmodmap -e "keycode 76 = End"           # F10 or F11
# (Adjust if necessary!)

#
# 2. Disable caps lock
#
setxkbmap -option caps:none

#
# 3. Write or update your ~/.xbindkeysrc with brightness + Caps Lock binding
#
cat <<EOF > ~/.xbindkeysrc
# Press F6 to simulate brightness down
"xdotool key XF86MonBrightnessDown"
    F6

# Press F7 to simulate brightness up
"xdotool key XF86MonBrightnessUp"
    F7

# Caps Lock as Ctrl+F
"xdotool key ctrl+f"
    Caps_Lock
EOF

#
# 4. Restart xbindkeys so the new bindings take effect
#
pkill xbindkeys
xbindkeys
