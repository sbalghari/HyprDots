#!/bin/bash

# Launch NetworkManager
nmcli networking on

# sleep 5

# Kill nm-applet to prevent it from appearing in the system tray
# if pgrep nm-applet > /dev/null; then
#     pkill nm-applet
# fi

exit 0