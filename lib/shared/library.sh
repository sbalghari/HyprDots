#!/bin/bash

# Import the logger
source lib/shared/logger.sh

# Function for checking if a package is installed
isInstalled() {
    local package="$1"

    # Check if the package is installed.
    if yay -Q "$package" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to install a package
installPackage() {
    local package="$1"

    # Install the package using yay.
    if ! isInstalled $package; then
        log "Info" "Installing $package..."
        yay -S --noconfirm --needed "$package"
        if [ $? -eq 0 ]; then
            log "Success" "$package installed successfully."
        else
            log "Error" "Failed to install $package."
        fi
    else
        log "Info" "Package $package is already installed."
    fi
}

# Function to install packages in groups
installPackages() {
    local package_group_name=$1
    local packages=("${!2}")

    # Install the packages in groups
    log "Info" "Installing $package_group_name packages..."
    for package in "${packages[@]}"; do
        installPackage "$package"
    done
    log "Success" "$package_group_name packages installation complete."
}
