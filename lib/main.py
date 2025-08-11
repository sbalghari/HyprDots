from install import DotfilesInstaller, install_wallpapers, install_dependencies
from options import install_optional_applications
from includes import print_hyprdots_title, print_subtext, print_success, print_error
from shared import LOG_FILE

from time import sleep
import os 
import sys

LOG_FILE = os.path.join(os.path.expanduser("~"), ".cache", "HyprDotsSetup.log")

if not sys.stdin.isatty():
    print("Error: This script must be run in a TTY-enabled terminal.")
    sys.exit(1)


def _title() -> None:
    print_hyprdots_title()
    print_subtext("Welcome to HyprDots installer!")
    print_subtext("A clean, full-featured, and aesthetic Hyprland dotfiles.")
    print_subtext("An open-source project by Saifullah Balghari")
    print()
    
def _clear() -> None:
    print("\033c", end="") 
    _title()
    
def _error_message(component_name: str) -> None:
    return f"{component_name} installation failed. Please check the logs for details."

def install() -> bool:
    _clear()
    
    dry_run = False  # Replaces the actual logic code with sleep statements.
    
    # Clear the log file
    open(LOG_FILE, "w").close()
    
    # Packages (dependencies)
    if not install_dependencies(dry_run=dry_run):
        print_error(_error_message("Packages"))
        return False
    
    # Dotfiles
    print()
    if not DotfilesInstaller(dry_run=dry_run).install():
        print_error(_error_message("Dotfiles"))
        return False

    # Wallpapers
    print()
    if not install_wallpapers(dry_run=dry_run):
        print_error(_error_message("Wallpapers"))
        return False
    
    # Optional Applications
    print()
    if not install_optional_applications(dry_run=dry_run):
        print_error(_error_message("Optional Applications"))
        return False
    
    if dry_run:
        sleep(2)
    return True

def main():
    if not install():
        print()
        print()
        print_error(f"HyprDots installation failed. Please check the logs for details: {LOG_FILE}")
        sys.exit()
    
    print()
    print()
    print_success("HyprDots installation completed successfully!")
    

if __name__ == "__main__":
    main()
    