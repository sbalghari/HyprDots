from includes import (
    print_info,
    print_success,
    print_header,
    install_package_group,
    is_installed
)
from shared import logger, log_heading

from time import sleep
from typing import Dict, List


core_utils: List[str] = [
        "atuin",
        "blueman",
        "bluez-utils",
        "brightnessctl",
        "btop",
        "cava",
        "checkupdates-with-aur",
        "eza",
        "fastfetch",
        "figlet",
        "python-requests",
        "fish",
        "htop",
        "gum",
        "neofetch",
        "neovim",
        "network-manager-applet",
        "wlogout",
        "yay",
        "zram-generator",
        "pavucontrol",
        "power-profiles-daemon",
        "rofi",
        "reflector",
        "udiskie",
        "uwsm",
        "flatpak",
        "sddm",
        "git",
        "waybar",
        "waypaper",
        "vim",
        "starship",
        "swaync",
        "swww",
        "firefox",
        "kitty"
    ]

hyprland: List[str] = [
        "hypridle",
        "hyprland",
        "hyprland-protocols",
        "hyprlock",
        "hyprpicker",
        "hyprpolkitagent",
        "hyprshade",
        "hyprshot",
        "xdg-desktop-portal-hyprland"
    ]

theming: List[str] = [
        "gtk-engine-murrine",
        "python-pywal",
        "tela-circle-icon-theme-standard",
        "bibata-cursor-theme-bin",
        "qt5-wayland",
        "qt5ct",
        "qt6-wayland",
        "qt6ct"
    ]

fonts: List[str] = [
        "noto-fonts",
        "ttf-dejavu",
        "ttf-firacode",
        "ttf-firacode-nerd",
        "ttf-font-awesome",
        "ttf-intone-nerd",
        "ttf-jetbrains-mono",
        "ttf-jetbrains-mono-nerd",
        "ttf-liberation",
        "ttf-nerd-fonts-symbols",
        "ttf-nerd-fonts-symbols-mono",
        "ttf-roboto"
    ]

applications: List[str] = [
        "smile",
        "nautilus",
        "nautilus-code",
        "nautilus-copy-path",
        "nautilus-hide",
        "mission-center",
        "visual-studio-code-bin",
        "freedownloadmanager",
    ]


def install_dependencies(dry_run: bool = False) -> bool:
    log_heading("Packages installer started")
    print_header("Installing packages.")
    
    groups: Dict[str, List[str]] = {
        "Core packages" : core_utils, 
        "Hyprland packages" : hyprland, 
        "Theming packages" : theming, 
        "Fonts" : fonts, 
        "Applications" : applications
    }
    
    print_info("Installing core dependencies, This might take a while. please be patient.")
    logger.info("Installing Dependencies...")
    if dry_run:
            sleep(2)
    if not dry_run:
        for title, packages_list in groups.items():
            packages_list = [pkg for pkg in packages_list if not is_installed(pkg)] # Filter out already installed packages
            if not install_package_group(group=packages_list, group_name=title):
                logger.error(f"Unable to install {title}")
                return False
    print_success("Successfully installed dependencies.")
    
    print()
    return True