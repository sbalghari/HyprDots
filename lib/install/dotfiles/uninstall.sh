#!/bin/bash

# Import the required functions
source lib/shared/library.sh
source lib/shared/logger.sh

# Paths
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

uninstallDotfiles() {
    # Restore ~/.config files and directories from original backup
    restoreFiles "$ORIGINAL_BACKUP_DIR/.config" "${HOME}/.config" DOT_CONFIG_DIRS[@]
    restoreFiles "$ORIGINAL_BACKUP_DIR/.config" "${HOME}/.config" DOT_CONFIG_FILES[@]

    # Remove the installation marker file
    if [ -f "$INSTALL_MARKER" ]; then
        rm "$INSTALL_MARKER"
        log "Info" "Installation marker removed: $INSTALL_MARKER"
    fi

    log "Success" "Dotfiles uninstalled successfully!"
}
