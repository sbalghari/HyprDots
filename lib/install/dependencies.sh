#!/bin/bash

# Import the required functions
source lib/shared/library.sh
source lib/shared/logger.sh

# Package groups
Hyprland=(
    hyprland
    hyprland-protocols
    hypridle
    hyprlock
    hyprpicker
    hyprpolkitagent
    hyprshade
    hyprshot
)

Fonts=(
    ttf-dejavu
    ttf-firacode
    ttf-firacode-nerd
    ttf-font-awesome
    ttf-intone-nerd
    ttf-jetbrains-mono
    ttf-jetbrains-mono-nerd
    ttf-liberation
    ttf-nerd-fonts-symbols
    ttf-nerd-fonts-symbols-mono
    ttf-roboto
    noto-fonts
)

Applications=(
    firefox
    kitty
    flatpak
    mission-center
    nautilus
    smile
)

Tools=(
    atuin
    btop
    brightnessctl
    cava
    eza
    fastfetch
    figlet
    gum
    neofetch
    neovim
    rofi
    starship
    swaync
    swww
    waybar
    waypaper
    wlogout
    xdotool
)

System=(
    brightnessctl
    checkupdates-with-aur
    efibootmgr
    fish
    iw
    networkmanager
    network-manager-applet
    power-profiles-daemon
    python-gobject
    reflector
    udiskie
    zram-generator
    alsa-utils
    blueman
    bluez
    bluez-utils
    pavucontrol
    pipewire
    pipewire-alsa
    pipewire-jack
    pipewire-pulse
    wireplumber
)

Appearance=(
    bibata-cursor-theme-bin
    tela-circle-icon-theme-standard
    gtk-engine-murrine
    python-pywal
    qt5-wayland
    qt5ct
    qt6ct
)

installDependencies() {
    # Install each package groups
    installPackages "Hyprland" Hyprland[@]
    installPackages "Fonts" Fonts[@]
    installPackages "Applications" Applications[@]
    installPackages "Tools" Tools[@]
    installPackages "System" System[@]
    installPackages "Appearance" Appearance[@]
}
