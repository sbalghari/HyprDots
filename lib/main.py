from install import DotfilesInstaller, install_wallpapers, install_dependencies
from options import install_optional_applications
from includes import print_hyprdots_title, print_subtext, print_success, print_error
from shared import LOG_FILE, HYPRDOTS_METADATA_FILE

from time import sleep
from typing import Dict, Callable
import sys
import argparse
import json

# Create an empty log file
open(LOG_FILE, "w").close()

DRY_RUN = False

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

def _install_components() -> bool:
    dry_run = DRY_RUN
    
    components: Dict[str, Callable] = {
        "Dependencies": install_dependencies(dry_run=dry_run),
        "Dotfiles": DotfilesInstaller(dry_run=dry_run).install(),
        "Wallpapers": install_wallpapers(dry_run=dry_run),
        "Optional Applications": install_optional_applications(dry_run=dry_run),
    }
    
    # Install components
    for component_name, install_function in components.items():
        if not install_function:
            print_error(_error_message(component_name))
            return False
            
    if dry_run:
        sleep(2)
        
    return True

def _get_version():
    try:
        with open(HYPRDOTS_METADATA_FILE, "r") as f:
            metadata = json.load(f)
            return metadata.get("version", "unknown")
    except Exception:
        return "unknown"

def install():
    _clear()
    if not _install_components():
        print()
        print()
        print_error(f"HyprDots installation failed. Please check the logs for details: {LOG_FILE}")
        sys.exit()
    print()
    print()
    print_success("HyprDots installation completed successfully!")

def uninstall():
    print("work in progress for this feature...")

def check_update():
    print("work in progress for this feature...")

def update():
    print("work in progress for this feature...")

def arg_parser(parser)-> argparse.Namespace:
    parser.add_argument(
        "-i", "--install", 
        action="store_true", 
        help="Installs HyprDots on your system", 
    )
    parser.add_argument(
        "-r", "--remove",
        action="store_true",
        help="Uninstalls HyprDots from your system"
    )
    parser.add_argument(
        "-u", "--update",
        action="store_true",
        help="Updates HyprDots to the latest version"
    )
    parser.add_argument(
        "-cu", "--check-update",
        action="store_true",
        help="Checks if a new version of HyprDots is available"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=_get_version(),
        help="Show program version and exit"
    )
    
    args = parser.parse_args()
    return args

def main():
    parser = argparse.ArgumentParser(
        description="HyprDots, a polished, feature-rich dotfiles for Arch Linux and Hyprland.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    args = arg_parser(parser)
    
    if args.install:
        install()
    elif args.remove:
        uninstall()
    elif args.update:
        update()
    elif args.check_update:
        check_update() 
    else:
        parser.print_help()
        sys.exit(0)
        
if __name__ == "__main__":
    main()
