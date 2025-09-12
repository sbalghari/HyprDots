from includes.logger import logger, log_heading
from includes.paths import LOG_FILE
from includes.tui import print_hyprdots_title, print_subtext, print_success, print_error, Spinner

from modules import DotfilesInstaller, WallpapersInstaller, PackagesInstaller

from misc.apply_gtk_theme import apply_gtk_theme
from misc.apply_wallpaper import apply_wallpaper
from misc.reload_hyprctl import reload_hyprland

from time import sleep
from typing import Dict, Callable
import sys


class HyprDotsInstaller:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

        # ensure log file is empty at start
        open(LOG_FILE, "w").close()
        log_heading("HyprDots is initialized")

    def _title(self) -> None:
        print_hyprdots_title()
        print_subtext("Welcome to HyprDots installer!")
        print_subtext(
            "A clean, full-featured, and aesthetic Hyprland dotfiles.")
        print_subtext("An open-source project by Saifullah Balghari")
        print()

    def _clear(self) -> None:
        print("\033c", end="")

    def _exit(self) -> None:
        print()
        print()
        print_error(
            f"HyprDots installation failed. Please check the logs for details: {LOG_FILE}"
        )
        sys.exit(1)

    def install_components(self) -> bool:
        logger.info("Starting installation of components...")

        components: Dict[str, Callable[[], bool]] = {
            "Packages": lambda: PackagesInstaller(dry_run=self.dry_run).install(),
            "Dotfiles": lambda: DotfilesInstaller(dry_run=self.dry_run).install(),
            "Wallpapers": lambda: WallpapersInstaller(dry_run=self.dry_run).install(),
        }

        for component_name, install_func in components.items():
            if not install_func():
                logger.error(
                    f"{component_name} installation failed. Please check the logs for details.")
                return False
            logger.info(f"{component_name} installed successfully.")

        sleep(1)  # delay for better UX
        return True

    def install(self) -> None:
        self._clear()
        self._title()

        if self.dry_run:
            print("Dry run mode enabled. No changes will be made.")
            print()

        logger.info("Starting HyprDots installation...")

        logger.info("Installing main components...")
        if not self.install_components():
            self._exit()

        if not PackagesInstaller(dry_run=self.dry_run).install_optional_applications():
            print_error(
                "Couldn't install optional applications, continuing...")
            

        # Finalizing
        log_heading("Finalization")
        with Spinner("Finalizing HyprDots installation...") as spinner:
            sleep(1)

            spinner.update_text("Reloading hyprland...")
            if not reload_hyprland():
                spinner.error("Hyprland reload failed.")
            
            sleep(1)
            spinner.update_text("Installing GTK Catppuccin theme...")
            if not apply_gtk_theme(spinner):
                spinner.error(
                    "Unable to install GTK theme, install manually later!")
                
            sleep(1)
            spinner.update_text("Applying wallpaper...")
            if not apply_wallpaper():
                spinner.error("Unable to apply wallpaper, apply manually.")

            sleep(1)
            spinner.success("Changes applied successfully.")

        print()
        print()
        print_success("HyprDots installation completed successfully!")
        sleep(2)
        sys.exit(0)
