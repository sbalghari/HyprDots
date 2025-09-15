from pathlib import Path

HOME = Path.home()

USER_CONFIGS_DIR = HOME / ".config"
USER_DOTFILES_DIR = HOME / "Dotfiles"
USER_WALLPAPERS_DIR = HOME / "Wallpapers"

SBDOTS_SHARE_DIR = Path("/usr/share/sbdots")
SBDOTS_DOTFILES_DIR = SBDOTS_SHARE_DIR / "dotfiles"
SBDOTS_WALLPAPERS_DIR = SBDOTS_SHARE_DIR / "wallpapers"
SBDOTS_METADATA_FILE = SBDOTS_SHARE_DIR / "metadata.json"

LOG_FILE = HOME / ".cache/sbdots_installer.log"

HYPRLAND_PKGS = SBDOTS_SHARE_DIR / "packages/hyprland.json"
CORE_PKGS = SBDOTS_SHARE_DIR / "packages/core.json"
FONTS = SBDOTS_SHARE_DIR / "packages/fonts.json"
APPLICATIONS = SBDOTS_SHARE_DIR / "packages/applications.json"
THEMING_PKGS = SBDOTS_SHARE_DIR / "packages/theming.json"
OPTIONAL_PKGS = SBDOTS_SHARE_DIR / "packages/optional.json"
