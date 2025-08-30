from pathlib import Path

HOME = Path.home()

USER_CONFIGS_DIR = HOME / "config"
USER_DOTFILES_DIR = HOME / "Dotfiles"
USER_WALLPAPERS_DIR = HOME / "Wallpapers"

HYPRDOTS_SHARE_DIR = Path("/usr/share/hyprdots")
HYPRDOTS_DOTFILES_DIR = HYPRDOTS_SHARE_DIR / "dotfiles"
HYPRDOTS_WALLPAPERS_DIR = HYPRDOTS_SHARE_DIR / "wallpapers"
HYPRDOTS_METADATA_FILE = HYPRDOTS_SHARE_DIR / "metadata.json"

LOG_FILE = HOME / ".cache/hyprdots_installer.log"