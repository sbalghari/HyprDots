from includes.logger import logger, log_heading
from includes.paths import HYPRLAND_PKGS, CORE_PKGS, FONTS, APPLICATIONS, THEMING_PKGS, OPTIONAL_PKGS
from includes.library import install_package_group, is_installed
from includes.tui import print_header, Spinner, checklist, print_success, print_info

from time import sleep
from typing import Dict, List
from pathlib import Path
import json


class PackagesInstaller:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run

        # Load package lists
        self.core: List[str] = self._get_packages_list(CORE_PKGS)
        self.hyprland: List[str] = self._get_packages_list(HYPRLAND_PKGS)
        self.applications: List[str] = self._get_packages_list(APPLICATIONS)
        self.fonts: List[str] = self._get_packages_list(FONTS)
        self.theming: List[str] = self._get_packages_list(THEMING_PKGS)
        self.optional: List[str] = self._get_packages_list(OPTIONAL_PKGS)

    def install(self) -> bool:
        log_heading("Packages installer started")
        print_header("Installing packages.")
        print()

        groups: Dict[str, List[str]] = {
            "Core packages": self.core,
            "Hyprland packages": self.hyprland,
            "Theming packages": self.theming,
            "Fonts": self.fonts,
            "Applications": self.applications,
        }

        print_info(
            "Installing packages(dependencies), This might take a while. please be patient."
        )
        logger.info("Installing packages(dependencies)...")

        if self.dry_run:
            sleep(2)
        else:
            for title, packages_list in groups.items():
                packages_list = [
                    pkg for pkg in packages_list if not is_installed(pkg)
                ]  # Filter out already installed packages
                if not packages_list:
                    logger.info(
                        f"All {title} are already installed, Skipping...")
                    continue
                if not install_package_group(group=packages_list, group_name=title):
                    logger.error(f"Unable to install {title}")
                    return False
        print_success("Successfully installed packages.")

        print()
        return True

    def install_optional_applications(self) -> bool:
        log_heading("Optional packages installer started")
        print_header("Installing optional applications.")
        print()

        chosen: List[str] = checklist(
            title="Chose apps to install.", items=self.optional
        )
        if chosen:
            logger.info(f"Chosen packages: {', '.join(chosen)}")
            with Spinner("Installing chosen applications...") as spinner:
                if self.dry_run:
                    sleep(2)
                else:
                    chosen = [
                        pkg for pkg in chosen if not is_installed(pkg)
                    ]  # Filter out already installed packages
                    if not chosen:
                        spinner.success(
                            "All chosen optional packages are already installed, Skipping..."
                        )
                        return True
                    if not install_package_group(
                        group=chosen, group_name="optional packages"
                    ):
                        spinner.error("Unable to install optional packages.")
                        return False
                spinner.success("Optional packages installed successfully.")
        else:
            logger.info("No optional packages selected, skipping...")

        return True

    def _get_packages_list(self, filepath: Path) -> List[str]:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError(
                        f"Expected a list in {filepath}, got {type(data)}")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if isinstance(e, FileNotFoundError):
                logger.error(f"Package list {filepath} not found.")
            else:
                logger.error(f"Package list {filepath} is not valid JSON.")
            raise
