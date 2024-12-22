#!/bin/bash

# Modified by:  Saifullah Balghari
# Original:     Stephen Raabe (ML4W)

SERVICE="hypridle"
if [[ "$1" == "status" ]]; then
    sleep 1
    if pgrep -x "$SERVICE" >/dev/null ;then
        echo '{"text": "RUNNING", "class": "active", "tooltip": "Screen locking active\nLeft: Deactivate\nRight: Lock Screen"}'
    else
        echo '{"text": "NOT RUNNING", "class": "notactive", "tooltip": "Screen locking deactivated\nLeft: Activate\nRight: Lock Screen"}'
    fi
fi
if [[ "$1" == "toggle" ]]; then
    if pgrep -x "$SERVICE" >/dev/null ;then
        killall hypridle
    else
        hypridle
    fi
fi