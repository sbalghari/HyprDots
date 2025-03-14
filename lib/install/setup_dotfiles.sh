#!/bin/bash

# Import the required functions
source lib/shared/library.sh
source lib/shared/logger.sh

# Paths
SOURCE_DOT_CONFIG="configs/.config"
SOURCE_DOT_USER_SETTINGS="configs/.user_settings"
BACKUP_DIR="$HOME/dotfiles/backup"
TARGET_DOTFILES_DIR="$HOME"

# ~/.config contents
DOT_CONFIG_DIRS=(
    atuin
    btop
    cava
    fastfetch
    fish
    hypr
    kitty
    neofetch
    nwg-dock-hyprland
    rofi
    swaync
    waybar
    waypaper
    wlogout
)
DOT_CONFIG_FILES=(
    starship.toml
)

# ~/.user_settings contents
DOT_USER_SETTINGS_FILES=(
    gtk_settings.json
    waybar_style.sh
)

# Check if the backup directory exists, create it if not
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    log "Info" "Backup directory created: $BACKUP_DIR"
fi

# Check if the ~/.config dir exists and create it if not
if [ ! -d "$TARGET_DOTFILES_DIR/.config" ]; then
    mkdir -p "$TARGET_DOTFILES_DIR/.config"
    log "Info" "Created ~/.config directory: $TARGET_DOTFILES_DIR/.config"
fi

# Check if the ~/.user_settings dir exists and create it if not
if [ ! -d "$TARGET_DOTFILES_DIR/.user_settings" ]; then
    mkdir -p "$TARGET_DOTFILES_DIR/.user_settings"
    log "Info" "Created ~/.user_settings directory: $TARGET_DOTFILES_DIR/.user_settings"
fi

# Check the owner of the ~/.config and ~/.user_settings and if it is not the user, change the owner manually to user
if [ "$(stat -c %U "$TARGET_DOTFILES_DIR/.config")" != "$(whoami)" ]; then
    log "Warning" "Changing ownership of ~/.config to $(whoami)..."
    sudo chown -R "$(whoami):$(whoami)" "$TARGET_DOTFILES_DIR/.config"
fi
if [ "$(stat -c %U "$TARGET_DOTFILES_DIR/.user_settings")" != "$(whoami)" ]; then
    log "Warning" "Changing ownership of ~/.user_settings to $(whoami)..."
    sudo chown -R "$(whoami):$(whoami)" "$TARGET_DOTFILES_DIR/.user_settings"
fi

# Backup existing ~/.config files
backupFiles "$TARGET_DOTFILES_DIR/.config" "$BACKUP_DIR/.config" DOT_CONFIG_DIRS[@]
backupFiles "$TARGET_DOTFILES_DIR/.config" "$BACKUP_DIR/.config" DOT_CONFIG_FILES[@]

# Backup existing ~/.user_settings files
backupFiles "$TARGET_DOTFILES_DIR/.user_settings" "$BACKUP_DIR/.user_settings" DOT_USER_SETTINGS_FILES[@]

# Copy new ~/.config files
copyFiles "$SOURCE_DOT_CONFIG" "$TARGET_DOTFILES_DIR/.config" DOT_CONFIG_DIRS[@]
copyFiles "$SOURCE_DOT_CONFIG" "$TARGET_DOTFILES_DIR/.config" DOT_CONFIG_FILES[@]

# Copy new ~/.user_settings files
copyFiles "$SOURCE_DOT_USER_SETTINGS" "$TARGET_DOTFILES_DIR/.user_settings" DOT_USER_SETTINGS_FILES[@]

log "Success" "Dotfiles setup completed successfully!"
