#!/bin/bash

# Check if an argument is passed
if [[ -z "$1" ]]; then
    echo "No arguments passed."
    echo "Usage: $0 change|restore"
    exit 1
fi

if [[ $1 == "change" ]]; then
    # Change wallpaper to a random one
    waypaper --random &
elif [[ $1 == "restore" ]]; then
    # Restore the previous wallpaper
    waypaper --restore
else
    echo "No args passed"
fi
