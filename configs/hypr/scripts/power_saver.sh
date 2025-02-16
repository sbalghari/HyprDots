#!/bin/bash

# Note: This script is used by Udev rules

# If the battery is charging
if [ "$1" == "plugged" ]; then
    # Resets the power profile and brightness levels
    brightnessctl set 100%
    powerprofilesctl set balanced

    # Notify
    notify-send -u critical  "Plugged!" "Balanced mode is enabled, press Super+SHIFT+M to toggle performance mode."
elif [ "$1" == "unplugged" ]; then
    # Enable power-saver and lower brightness th 50%
    brightnessctl set 50%
    powerprofilesctl set power-saver

    # Notify
    notify-send -u critical  "Unplugged!" "Power-saver is enabled to improve battery life." 
fi

