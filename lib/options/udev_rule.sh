#!/bin/bash

# This script will install a udev rule that enables
# power saver and lower brightness levels on laptops
# automatically when plugged-out (Optional: only for laptops)

# Import logger
source lib/shared/logger.sh

UDEV_RULE_DIR="/usr/lib/udev/rules.d"
UDEV_RULE_FILE="lib/udev/rules.d/99-power-state.rules"

installUdevRule() {
    # Check if the udev rule directory exists
    if [ ! -d "$UDEV_RULE_DIR" ]; then
        log "Error" "Udev rule directory '$UDEV_RULE_DIR' does not exist."
        exit 1
    fi

    # Check if the udev rule file already exists
    if [ -f "$UDEV_RULE_DIR/99-power-state.rules" ]; then
        log "Warning" "Udev rule file '$UDEV_RULE_DIR/99-power-state.rules' already exists."
        log "Info" "Skipping rule installation."
        exit 0
    fi

    # Install the udev rule file
    log "Info" "Installing udev rule..."
    sudo cp "$UDEV_RULE_FILE" "$UDEV_RULE_DIR"
    if [[ $? -eq 0 ]]; then
        log "Info" "Installed $UDEV_RULE_FILE"
        exit 0
    else
        log "Error" "Failed to install $UDEV_RULE_FILE"
        exit 1
    fi
}
