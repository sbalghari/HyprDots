#!/bin/bash

# By:  Saifullah Balghari

# Paths
DUNST_CONFIG="$HOME/.config/dunst/dunstrc"
DUNST_BACKUP="$DUNST_CONFIG.backup"
WAL_COLORS="$HOME/.cache/wal/colors"

# Ensure a backup exists
if [ ! -f "$DUNST_BACKUP" ]; then
    echo "Creating a backup of the Dunst config."
    cp "$DUNST_CONFIG" "$DUNST_BACKUP"
fi

# Restore the original config with placeholders
cp "$DUNST_BACKUP" "$DUNST_CONFIG"

# Extract Pywal colors
WAL_FRAME=$(sed -n '12p' "$WAL_COLORS") # Line 12: color11

# Replace placeholders in the Dunst config
sed -i "s/WAL_FRAME/\"$WAL_FRAME\"/g" "$DUNST_CONFIG"

echo "Dunst colors updated with Pywal colors."
