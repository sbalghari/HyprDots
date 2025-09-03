from modules import DotfilesInstaller, WallpapersInstaller, PackagesInstaller
from includes.logger import logger, log_heading
from includes.paths import LOG_FILE
from includes.tui import Spinner, print_hyprdots_title, print_subtext, print_success, print_error
from includes.library import get_version

from time import sleep
import subprocess
from typing import Dict, Callable
import sys
import argparse


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

    def _install_components(self) -> bool:
        logger.info("Starting installation of components...")
        components: Dict[str, Callable[[], bool]] = {
            "Packages": lambda: PackagesInstaller(dry_run=self.dry_run).install(),
            "Dotfiles": lambda: DotfilesInstaller(dry_run=self.dry_run).install(),
            "Wallpapers": lambda: WallpapersInstaller(dry_run=self.dry_run).install(),
            "Optional Applications": lambda: PackagesInstaller(
                dry_run=self.dry_run
            ).install_optional_applications(),
        }

        for component_name, install_func in components.items():
            if not install_func():
                logger.error(
                    f"{component_name} installation failed. Please check the logs for details.")
                return False
            logger.info(f"{component_name} installed successfully.")

        sleep(1)  # delay for better UX
        return True

    def _apply_gtk_theme(self) -> bool:
        """Apply GTK theme using gtk_theme_manager."""
        log_heading("Applying GTK theme")
        logger.info("Applying GTK theme...")
        print()
        try:
            with Spinner("Applying GTK theme...") as spinner:
                sleep(1)

                logger.info("Installing Catppuccin theme...")
                spinner.update_text("Downloading Catppuccin theme...")
                subprocess.run(
                    ["catppuccin_theme_installer", "mocha", "blue"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                logger.info("Applying Catppuccin theme...")
                spinner.update_text("Applying Catppuccin theme...")
                subprocess.run(
                    [
                        "gtk_theme_manager",
                        "-t",
                        "catppuccin-mocha-blue-standard+default",
                        "-i",
                        "Tela-circle-dark",
                        "-c",
                        "Bibata-Original-Classic",
                        "-s",
                        "20",
                        "-m",
                        "prefer_dark",
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                spinner.success("GTK theme applied successfully.")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd} (exit code {e.returncode})")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while applying GTK theme: {e}")
            return False

    def install(self) -> None:
        self._clear()
        self._title()

        if self.dry_run:
            print("Dry run mode enabled. No changes will be made.")
            print()

        logger.info("Starting HyprDots installation...")
        if not self._install_components() or not self._apply_gtk_theme():
            print()
            print()
            print_error(
                f"HyprDots installation failed. Please check the logs for details: {LOG_FILE}"
            )
            sys.exit(1)

        print()
        print()
        print_success("HyprDots installation completed successfully!")

    def uninstall(self) -> None:
        print("This feature is not available yet!")

    def check_update(self) -> None:
        print("This feature is not available yet!")

    def update(self) -> None:
        print("This feature is not available yet!")

    def arg_parser(self, parser) -> argparse.Namespace:
        parser.add_argument(
            "-i",
            "--install",
            action="store_true",
            help="Installs HyprDots on your system",
        )
        parser.add_argument(
            "-r",
            "--remove",
            action="store_true",
            help="Uninstalls HyprDots from your system",
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Updates HyprDots to the latest version",
        )
        parser.add_argument(
            "-cu",
            "--check-update",
            action="store_true",
            help="Checks if a new version of HyprDots is available",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=get_version(),
            help="Show program version and exit",
        )
        return parser.parse_args()

    def main(self) -> None:
        parser = argparse.ArgumentParser(
            description="HyprDots, a polished, feature-rich dotfiles for Arch Linux and Hyprland.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        args = self.arg_parser(parser)

        if args.install:
            self.install()
        elif args.remove:
            self.uninstall()
        elif args.update:
            self.update()
        elif args.check_update:
            self.check_update()
        else:
            parser.print_help()
            sys.exit(0)


if __name__ == "__main__":
    installer = HyprDotsInstaller(dry_run=False)
    installer.main()
