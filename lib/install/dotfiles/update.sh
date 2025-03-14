#!/bin/bash

# Import the required functions
source lib/shared/library.sh
source lib/shared/logger.sh

# Paths
SOURCE_DOT_CONFIG="configs/.config"
SOURCE_DOT_USER_SETTINGS="configs/.user_settings"
SBHD_DIR="$HOME/sbhd/"
BACKUP_DIR="$SBHD_DIR/backup"
UPDATE_BACKUP_DIR="$BACKUP_DIR/updates"
ORIGINAL_BACKUP_DIR="$BACKUP_DIR/original"
INSTALL_MARKER="$SBHD_DIR/.installed"

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

updateDotfiles() {
    # Check if dotfiles are installed
    if [ ! -f "$INSTALL_MARKER" ]; then
        log "Error" "Dotfiles are not installed. Run the setup script first."
        exit 1
    fi

    # Check if the update backup directory exists, create it if not
    if [ ! -d "$UPDATE_BACKUP_DIR" ]; then
        mkdir -p "$UPDATE_BACKUP_DIR"
        log "Info" "Update backup directory created: $UPDATE_BACKUP_DIR"
    fi

    # Backup ~/.config files
    backupFiles "${HOME}/.config" "$UPDATE_BACKUP_DIR/.config" DOT_CONFIG_DIRS[@]
    backupFiles "${HOME}/.config" "$UPDATE_BACKUP_DIR/.config" DOT_CONFIG_FILES[@]

    # Copy new ~/.config files
    copyFiles "$SOURCE_DOT_CONFIG" "${HOME}/.config" DOT_CONFIG_DIRS[@]
    copyFiles "$SOURCE_DOT_CONFIG" "${HOME}/.config" DOT_CONFIG_FILES[@]

    log "Success" "Dotfiles updated successfully!"
}
