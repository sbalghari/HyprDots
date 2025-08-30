from includes import (
    print_header,
    remove,
    check_configs_exists,
    create_symlink,
    Spinner,
)
from shared import (
    logger, 
    log_heading,
    USER_CONFIGS_DIR,
    USER_DOTFILES_DIR,
    HYPRDOTS_DOTFILES_DIR,
)

from pathlib import Path
import shutil
from time import sleep
from subprocess import run as run_command


class DotfilesInstaller:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.dotfiles_components = [
            "hypr", "waybar", "rofi", "fish", "kitty", "neofetch",
            "fastfetch", "cava", "waypaper", "swaync", "btop",
            "wlogout", "atuin", "starship.toml"
        ]

        self.source_dotfiles_components_paths = [
            HYPRDOTS_DOTFILES_DIR / i for i in self.dotfiles_components
        ]
        self.target_dotfiles_components_paths = [
            USER_DOTFILES_DIR / i for i in self.dotfiles_components
        ]

    def install(self):
        log_heading("Dotfiles installer started")
        print_header("Installing dotfiles.")

        with Spinner("Installing dotfiles...") as spinner:
            if not self._validate_sources(spinner):
                return False
            if not self._copy_dotfiles(spinner):
                return False
            if not self._verify_copy(spinner):
                return False
            if not self._remove_existing_configs(spinner):
                return False
            if not self._create_links(spinner):
                return False
            self._reload_hyprland(spinner)

            spinner.success("Dotfiles installed successfully!")
            logger.info("Dotfiles installed successfully!")
        
        print()
        return True

    def _validate_sources(self, spinner) -> bool:
        logger.info("Validating source dotfiles components.")
        spinner.update_text("Validating source dotfiles components...")
        if self.dry_run:
            sleep(2)
            return True
        for i in self.source_dotfiles_components_paths:
            if not check_configs_exists(i):
                logger.error(f"Missing source: {i}.")
                spinner.error(f"Missing source: {i}, exiting...")
                return False
        return True

    def _copy_dotfiles(self, spinner) -> bool:
        logger.info(f"Copying dotfiles to {USER_DOTFILES_DIR}")
        spinner.update_text("Copying dotfiles...")
        if self.dry_run:
            sleep(2)
            return True
        logger.info("Creating dotfiles dir...")
        if USER_DOTFILES_DIR.exists():
            logger.info("Dotfiles dir already exists, removing it...")
            remove(USER_DOTFILES_DIR)
        logger.info("Copying...")
        try:
            shutil.copytree(HYPRDOTS_DOTFILES_DIR, USER_DOTFILES_DIR)
        except Exception as e:
            logger.error(f"Failed to copy dotfiles: {e}")
            spinner.error("Failed to copy dotfiles.")
            return False
        return True

    def _verify_copy(self, spinner) -> bool:
        logger.info("Checking if copied successfully or not.")
        if self.dry_run:
            return True
        for i in self.target_dotfiles_components_paths:
            if not check_configs_exists(i):
                spinner.error(f"Copied dotfile component {i} is missing.")
                return False
        return True

    def _remove_existing_configs(self, spinner) -> bool:
        logger.info("Removing existing configs.")
        spinner.update_text("Removing existing configs...")
        if self.dry_run:
            sleep(2)
            return True
        for i in self.dotfiles_components:
            file: Path = USER_CONFIGS_DIR / i
            if not remove(file):
                spinner.error(f"Failed to remove existing config: {file}.")
                return False
        return True

    def _create_links(self, spinner) -> bool:
        logger.info("Creating system links.")
        spinner.update_text("Linking new dotfiles...")
        if self.dry_run:
            sleep(2)
            return True
        for component in self.dotfiles_components:
            source: Path = USER_DOTFILES_DIR / component
            target: Path = USER_CONFIGS_DIR / component
            if not create_symlink(source, target):
                spinner.error(f"Failed to link {source} to {target}.")
                return False
        return True

    def _reload_hyprland(self, spinner) -> None:
        if self.dry_run:
            return
        logger.info("Reloading Hyprland...")
        spinner.update_text("Reloading Hyprland...")
        sleep(1)
        run_command(["hyprctl", "reload"])
