#!/bin/bash

# Start the Bluetooth service
sudo systemctl start bluetooth
blueman-applet

# sleep 5

# Kill blueman-applet to prevent it from appearing in the system tray
# if pgrep blueman-applet > /dev/null; then
# pkill blueman-applet
# fi

exit 0