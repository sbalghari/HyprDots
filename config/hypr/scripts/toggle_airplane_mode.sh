#!/bin/bash

# Check if rfkill is installed
if ! command -v rfkill &>/dev/null; then
    notify-send "rfkill is not installed!" "Please install it to use this script."
    exit 1
fi

# Get the current state of all radios
airplane_mode=$(rfkill list | grep -i "Soft blocked: yes" | wc -l)
total_radios=$(rfkill list | grep -i "Soft blocked" | wc -l)

# Determine action based on the current state
if [ "$airplane_mode" -eq "$total_radios" ]; then
    echo "Disabling Airplane Mode..."
    rfkill unblock all
    echo "Airplane Mode Disabled."
    notify-send "Airplane Mode Disabled"
else
    echo "Enabling Airplane Mode..."
    rfkill block all
    echo "Airplane Mode Enabled."
    notify-send "Airplane Mode Enabled"
fi
