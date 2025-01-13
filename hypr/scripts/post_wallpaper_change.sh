#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_your_wallpaper>"
    exit 1
fi

sleep 1

# Generate pywal colors from the wallpaper
echo "Generating pywal colors..."
wal -i "$1"
echo "Generated pywal colors"

# Reload with the new colors
echo "Reloading waybar and swaync"
pkill waybar
pkill swaync 
swaync &
waybar &
echo "Successfully reloaded waybar and swaync"

sleep 0.2
echo "Running script..."
# This will convert wal color (color11 and color0) into ARGB for hyprland's borders
~/.config/hypr/scripts/update_hyprland_colors.sh

# This will store a blured version of the current wallpaper for hyprlock's background
~/.config/hypr/scripts/cache_wallpaper.sh "$1"

echo "Successfully ran the scripts"

hyprctl reloadR