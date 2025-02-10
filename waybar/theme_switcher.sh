#!/bin/bash

WAYBAR_DIR="$HOME/.config/waybar"
THEMES_DIR="$WAYBAR_DIR/themes"

# Check if a theme name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <theme-name>"
  exit 1
fi

THEME_NAME="$1"
THEME_PATH="$THEMES_DIR/$THEME_NAME"

# Copy theme files to the main directory
cp "$THEME_PATH/config.jsonc" "$WAYBAR_DIR/config.jsonc" 2>/dev/null || echo ":: No config.jsonc found for theme '$THEME_NAME'."
cp "$THEME_PATH/style.css" "$WAYBAR_DIR/style.css" 2>/dev/null || echo ":: No style.css found for theme '$THEME_NAME'."

# Restart Waybar to apply changes
killall waybar
waybar & disown

echo ":: Theme '$THEME_NAME' applied successfully!"
