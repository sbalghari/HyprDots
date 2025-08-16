import os

HOME = os.path.expanduser("~")

USER_CONFIGS_DIR = os.path.join(HOME, ".config")
USER_DOTFILES_DIR = os.path.join(HOME, "Dotfiles")
USER_WALLPAPERS_DIR = os.path.join(HOME, "Wallpapers")

HYPRDOTS_SHARE_DIR = "/usr/share/hyprdots"
HYPRDOTS_DOTFILES_DIR = os.path.join(HYPRDOTS_SHARE_DIR, "dotfiles")
HYPRDOTS_WALLPAPERS_DIR = os.path.join(HYPRDOTS_SHARE_DIR, "wallpapers")

LOG_FILE = os.path.join(os.path.expanduser("~"), ".cache", "hyprdots_installer.log")