from includes.logger import logger, log_heading
from includes.paths import HYPRLAND_PKGS, CORE_PKGS, FONTS, APPLICATIONS, THEMING_PKGS, OPTIONAL_PKGS
from includes.library import is_installed, install_package, remove_package, SudoKeepAlive
from includes.tui import print_header, Spinner, checklist, print_success, print_info, print_error, confirm

from time import sleep
from typing import Dict, List
from pathlib import Path
import subprocess
import json

# Note: yay is used instead of vanilla pacman for installing and removing packages


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
            return True

        # Remove conflicts if they exist
        conflicts: list[str] = [pkg for pkg in [
            'wofi', 'dunst'] if is_installed(pkg)]

        if conflicts:
            logger.info(f"Found conflicts: {conflicts}, removing them...")
            print_info("Removing conflicting packages...")

            failed_removals: list[str] = []
            for pkg in conflicts:
                with Spinner(f"Removing {pkg}") as spinner:
                    if remove_package(pkg):
                        spinner.success(f"Removed {pkg}")
                    else:
                        spinner.error(f"Failed to remove {pkg}")
                        failed_removals.append(pkg)

            if failed_removals:
                print_error(
                    f"Failed to remove conflicting packages: {failed_removals}")
                print_error(
                    "Installation will continue but HyprDots may act unexpectedly.")
                print_error("Please remove them manually!")
            else:
                print_success(
                    "All conflicting packages removed successfully!")

        for title, packages_list in groups.items():
            with Spinner(f"Installing {title}") as spinner:
                sleep(1)

                # Filter out already installed packages
                packages_list = [
                    pkg for pkg in packages_list if not is_installed(pkg)
                ]

                if not packages_list:
                    logger.info(
                        f"All {title} are already installed, Skipping.")
                    spinner.success(
                        f"{title} are already installed, skipping...")
                    continue

                failed_pkgs: List = []
                for pkg in packages_list:
                    spinner.update_text(f"Installing package: {pkg}")
                    if not install_package(pkg):
                        spinner.error(
                            f"Couldn't install package: {pkg}")
                        failed_pkgs.append(pkg)

                if failed_pkgs:
                    logger.error(
                        f"Error installing packages: {failed_pkgs}")
                    return False
                spinner.success(f"Successfully installed {title}.")

        print()
        return True

    def install_optional_applications(self) -> bool:
        log_heading("Optional packages installer started")
        print_header("Installing optional applications.")
        print()

        if self.dry_run:
            sleep(2)
            return True

        chosen: List[str] = checklist(
            title="Choose apps to install.", items=self.optional
        )

        if not chosen:
            logger.info("No optional packages selected, skipping...")
            print_info("No optional packages selected, skipping...")
            print()
            return True

        logger.info(f"Chosen packages: {', '.join(chosen)}")

        # Filter out already installed packages
        chosen = [pkg for pkg in chosen if not is_installed(pkg)]

        if not chosen:
            print_success(
                "All chosen optional packages are already installed, skipping...")
            logger.info(
                "All chosen optional packages are already installed, skipping...")
            print()
            return True

        failed_pkgs: List[str] = []

        with SudoKeepAlive(max_duration=1800) as sudo:  # 30 minutes max duration
            for pkg in chosen:
                with Spinner(
                    f"Installing {pkg}",
                    sudo_keepalive=sudo,  # Pass the keepalive instance for sudo monitoring
                ) as spinner:
                    try:
                        # Update spinner text with more detailed information
                        spinner.update_text(f"Installing {pkg}...")

                        # Attempt to install the package
                        if install_package(pkg):
                            spinner.success(f"Installed {pkg}", log=True)
                        else:
                            spinner.error(f"Failed to install {pkg}", log=True)
                            failed_pkgs.append(pkg)

                    except subprocess.TimeoutExpired:
                        spinner.error(
                            f"Timeout while installing {pkg}", log=True)
                        failed_pkgs.append(pkg)

                    except subprocess.CalledProcessError as e:
                        spinner.error(
                            f"Error installing {pkg}: {str(e)}", log=True)
                        failed_pkgs.append(pkg)

                    except Exception as e:
                        spinner.error(
                            f"Unexpected error installing {pkg}: {str(e)}", log=True)
                        failed_pkgs.append(pkg)

        if failed_pkgs:
            print_error(
                f"Failed to install {len(failed_pkgs)} package(s): {', '.join(failed_pkgs)}")
            logger.error(f"Error installing packages: {failed_pkgs}")

            # Ask if user wants to retry failed installations
            if confirm("Would you like to retry failed installations?"):
                return self._retry_failed_installations(failed_pkgs)

            return False
        else:
            print_success("All optional packages installed successfully!")
            logger.info("All optional packages installed successfully!")

        print()
        return True

    def _retry_failed_installations(self, failed_pkgs: List[str]) -> bool:
        """Retry installation of failed packages"""
        print_header("Retrying failed installations")

        retry_failed: List[str] = []

        with SudoKeepAlive(max_duration=1200) as sudo:  # 20 minutes for retry
            for pkg in failed_pkgs:
                with Spinner(
                    f"Retrying installation of {pkg}",
                    sudo_keepalive=sudo,
                    monitor_sudo=True
                ) as spinner:
                    try:
                        spinner.update_text(f"Retrying {pkg}...")

                        if install_package(pkg):
                            spinner.success(
                                f"Successfully installed {pkg} on retry", log=True)
                        else:
                            spinner.error(
                                f"Still failed to install {pkg}", log=True)
                            retry_failed.append(pkg)

                    except Exception as e:
                        spinner.error(
                            f"Error during retry of {pkg}: {str(e)}", log=True)
                        retry_failed.append(pkg)

        if retry_failed:
            print_error(
                f"Still failed to install {len(retry_failed)} package(s) after retry: {', '.join(retry_failed)}")
            logger.error(f"Packages still failed after retry: {retry_failed}")
            return False

        print_success(
            "All previously failed packages installed successfully on retry!")
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
