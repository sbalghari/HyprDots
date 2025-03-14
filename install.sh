#!/bin/bash

# Import Logger
source lib/shared/logger.sh

# Installer sources
log "Info" "Importing sources"
source lib/install/dependencies.sh
source lib/install/binaries.sh
source lib/install/dotfiles/install.sh
source lib/install/wallpapers.sh
source lib/options/udev_rules.sh
log "Success" "Successfully imported the sources"

# Main dir to save dotfile's configs
LOCAL_DIR="$HOME/sbhd"
if [ ! -d "$LOCAL_DIR" ]; then
    mkdir -p "$LOCAL_DIR"
    log "Info" "Directory created: $LOCAL_DIR"
fi

# Installer dependencies
INSTALL_DEP=("figlet" "gum")

# Install yay if not installed
if ! command -v yay &> /dev/null; then
    log "Info" "yay not found. Installing yay..."
    git clone https://aur.archlinux.org/yay.git /tmp/yay
    cd /tmp/yay
    makepkg -si
    cd -
    log "Success" "yay installed successfully."
else
    log "Info" "yay is already installed."
fi

# Install installer dependencies
for dep in "${INSTALL_DEP[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        log "Info" "$dep not found. Installing $dep..."
        yay -S "$dep" --noconfirm
        if [ $? -eq 0 ]; then
            log "Success" "$dep installed successfully."
        else
            log "Error" "Failed to install $dep."
            exit 1
        fi
    else
        log "Info" "$dep is already installed."
    fi
done

# Main install function
install() {
    # Install dependencies
    log "Info" "Installing Dependencies.."
    figlet "Installing Dependencies.." -w 100 | gum style --border="rounded" --border-foreground="#FF00FF" --padding="1 2" --margin="1"
    if installDependencies; then
        log "Success" "Dependencies installed successfully."
    else
        log "Error" "Failed to install dependencies."
        exit 1
    fi

    # Install binaries
    log "Info" "Installing Binaries.."
    figlet "Installing Binaries.." -w 100 | gum style --border="rounded" --border-foreground="#00FF00" --padding="1 2" --margin="1"
    if installBinaries; then
        log "Success" "Binaries installed successfully."
    else
        log "Error" "Failed to install binaries."
        exit 1
    fi

    # Installing Dotfiles
    log "Info" "Installing Dotfiles.."
    figlet "Installing Dotfiles.." -w 100 | gum style --border="rounded" --border-foreground="#00FFFF" --padding="1 2" --margin="1"
    if installDotfiles; then
        log "Success" "Dotfiles installed successfully."
    else
        log "Error" "Failed to install dotfiles."
        exit 1
    fi

    # Installing Wallpapers
    log "Info" "Installing Wallpapers.."
    figlet "Installing Wallpapers.." -w 100 | gum style --border="rounded" --border-foreground="#FFFF00" --padding="1 2" --margin="1"
    if installWallpapers; then
        log "Success" "Wallpapers installed successfully."
    else
        log "Error" "Failed to install wallpapers."
        exit 1
    fi
}

# Run the install function
install

log "Success" "Installation completed successfully!"
figlet "All Done!" -w 100 | gum style --border="rounded" --border-foreground="#00FF00" --padding="1 2" --margin="1"