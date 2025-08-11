#!/bin/bash

# Reload Hyprland configuration
hyprctl reload

# Reload swww daemon
killall swww-daemon
sleep 0.2
swww-daemon &

# Reload waybar
killall waybar
sleep 0.2
waybar &