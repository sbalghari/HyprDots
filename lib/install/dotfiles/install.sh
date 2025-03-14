#!/bin/bash

# Import the required functions
source lib/shared/library.sh
source lib/shared/logger.sh

# Paths
SOURCE_DOT_CONFIG="configs/.config"
SBHD_DIR="$HOME/sbhd/"
BACKUP_DIR="$SBHD_DIR/backup"
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

installDotfiles() {
    # Check if dotfiles are already installed
    if [ -f "$INSTALL_MARKER" ]; then
        log "Warning" "Dotfiles are already installed. Run the update script to update."
        exit 0
    fi

    # Check if the backup directory exists, create it if note
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        log "Info" "Backup directory created: $BACKUP_DIR"
    fi

    # Check if the original backup directory exists, create it if not
    if [ ! -d "$ORIGINAL_BACKUP_DIR" ]; then
        mkdir -p "$ORIGINAL_BACKUP_DIR"
        log "Info" "Original backup directory created: $ORIGINAL_BACKUP_DIR"
    fi

    # Backup ~/.config files
    backupFiles "${HOME}/.config" "$ORIGINAL_BACKUP_DIR/.config" DOT_CONFIG_DIRS[@]
    backupFiles "${HOME}/.config" "$ORIGINAL_BACKUP_DIR/.config" DOT_CONFIG_FILES[@]

    # Copy new ~/.config files and directories
    copyFiles "$SOURCE_DOT_CONFIG" "${HOME}/.config" DOT_CONFIG_DIRS[@]
    copyFiles "$SOURCE_DOT_CONFIG" "${HOME}/.config" DOT_CONFIG_FILES[@]

    # Create the installation marker file
    touch "$INSTALL_MARKER"
    log "Info" "Installation marker created: $INSTALL_MARKER"

    log "Success" "Dotfiles installed successfully!"
}
