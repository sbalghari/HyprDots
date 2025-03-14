#!/bin/bash

# Installs binaries from the dotfiles bin directory to /usr/local/bin

# Import logger
source lib/shared/logger.sh

# Define paths
DOTFILES_BIN_DIR="bin"
SYSTEM_BIN_DIR="/usr/local/bin"

installBinaries() {
  # Check if the dotfiles bin directory exists
  if [[ ! -d "$DOTFILES_BIN_DIR" ]]; then
    log "Error" "Dotfiles bin directory not found at $DOTFILES_BIN_DIR"
    exit 1
  fi

  # Check if /usr/local/bin exists and create it if not already exists
  if [[ ! -d "$SYSTEM_BIN_DIR" ]]; then
    log "Error" "System bin directory not found at $SYSTEM_BIN_DIR"

    # Create the system bin directory
    log "Info" "Creating system bin directory at $SYSTEM_BIN_DIR"
    mkdir -p "$SYSTEM_BIN_DIR"
    if [[ $? -ne 0 ]]; then
      log "Error" "Failed to create system bin directory at $SYSTEM_BIN_DIR"
      exit 1
    fi
  fi

  # Copy binaries from dotfiles/bin to /usr/local/bin
  log "Info" "Installing binaries from $DOTFILES_BIN_DIR to $SYSTEM_BIN_DIR..."
  for binary in "$DOTFILES_BIN_DIR"/*; do
    if [[ -f "$binary" && -x "$binary" ]]; then
      binary_name=$(basename "$binary")
      if [[ -e "$SYSTEM_BIN_DIR/$binary_name" ]]; then
        log "Warning" "$binary_name already exists in $SYSTEM_BIN_DIR. Skipping."
      else
        sudo cp "$binary" "$SYSTEM_BIN_DIR/$binary_name"
        if [[ $? -eq 0 ]]; then
          log "Info" "Installed $binary_name"
        else
          log "Info" "Failed to install $binary_name"
        fi
      fi
    fi
  done
}
