#!/bin/bash

# Import required functions
source lib/shared/logger.sh
source lib/shared/library.sh

# Paths
SOURCE_DIR="configs/Wallpapers"
TARGET_DIR="$HOME/Wallpapers"

WALLPAPERS=(
    avatar.png
    dark.png
    light.png
)

installWallpapers() {
    # Check if the backup directory exists, create it if not
    if [ ! -d "$TARGET_DIR" ]; then
        mkdir -p "$TARGET_DIR"
        log "Info" "Wallpapers directory created: $TARGET_DIR"
    fi

    # Install wallpapers
    log "info" "Installing wallpapers"
    copyFiles "$SOURCE_DIR" "$TARGET_DIR" WALLPAPERS[@]
}
