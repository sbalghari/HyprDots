#!/bin/bash

SWAYNC_DIR="$HOME/.config/swaync"
THEMES_DIR="$SWAYNC_DIR/themes"

# Check if a theme name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <theme-name>"
  exit 1
fi

THEME_NAME="$1"
THEME_PATH="$THEMES_DIR/$THEME_NAME"

# Copy theme files to the main directory
cp "$THEME_PATH/style.css" "$SWAYNC_DIR/style.css" 2>/dev/null || echo ":: No style.css found for theme '$THEME_NAME'."

# Restart Swaync to apply changes
killall swaync
swaync & disown

echo ":: Theme '$THEME_NAME' applied successfully!"
