#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_your_wallpaper>"
    exit 1
fi

sleep 1

echo "Generating pywal colors..."
wal -i "$1"
echo "Generated pywal colors"

echo "Reloading waybar and swaync"
pkill waybar
pkill swaync 
swaync &
waybar &
echo "Successfully reloaded waybar and swaync"

sleep 0.2

echo "Running script..."
~/.config/hypr/scripts/update_hyprland_colors.sh
~/.config/hypr/scripts/cache_wallpaper.sh "$1"
echo "Successfully ran the scripts"

hyprctl reload