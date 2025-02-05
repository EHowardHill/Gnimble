#!/bin/bash

#  Write a bash script that will remap a Debian 12 instance running Xorg. The following keys must be altered to perform the following functions:

# F1: Back key (browser)
# F2: Forward key (browser)
# F3: Refresh key (browser)
# F6: lower brightness
# F7: raise brightness
# F8: Home key
# F9: Page Down
# F10: Page Up
# F11: End key

# Remap keys using xmodmap
xmodmap -e "keycode 67 = XF86Back"      # F1 -> Back key (browser)
xmodmap -e "keycode 68 = XF86Forward"   # F2 -> Forward key (browser)
xmodmap -e "keycode 69 = XF86Refresh"   # F3 -> Refresh key (browser)
xmodmap -e "keycode 73 = Home"          # F8 -> Home key
xmodmap -e "keycode 74 = Prior"         # F9 -> Page Down
xmodmap -e "keycode 75 = Next"          # F10 -> Page Up
xmodmap -e "keycode 76 = End"           # F11 -> End key

# Brightness
xbindkeys -e "F6"  'xdotool key XF86MonBrightnessDown'
xbindkeys -e "F7"  'xdotool key XF86MonBrightnessUp'

# Disable Caps Lock (turn it off temporarily)
setxkbmap -option caps:none

# Bind Caps Lock to simulate "Ctrl+F"
xbindkeys -e "Caps_Lock" 'xdotool key ctrl+f'

# Reload xbindkeys (if using it to manage key bindings for actions like brightness)
pkill xbindkeys && xbindkeys &