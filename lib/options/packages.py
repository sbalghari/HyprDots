from includes import (
    print_info,
    checklist,
    Spinner,
    print_header,
    install_package_group,
    is_installed
)
from shared import logger, log_heading

from time import sleep
from typing import List


optional_applications: List[str] = [
    "gnome-text-editor",
    "youtube-music-bin",
    "syncthing",
    "vlc",
]
        
def install_optional_applications(dry_run: bool = False) -> bool:
    print_header("Installing optional applications.")
    log_heading("Optional applications installer started")
    
    chosen: List[str] = checklist(title="Chose apps to install.", items=optional_applications)
    if chosen:
        logger.info(f"Installing optional packages: {', '.join(chosen)}")
        with Spinner("Installing chosen applications...")as spinner:
            if dry_run:
                sleep(2)
            else:
                chosen = [pkg for pkg in chosen if not is_installed(pkg)] # Filter out already installed packages
                if not install_package_group(group=chosen, group_name="optional packages"):
                    logger.error("Unable to install optional packages.")
                    spinner.error("Unable to install optional packages.")
                    return False
            spinner.success("Optional packages installed successfully.")
    else:
        logger.info("No optional packages selected, skipping...")
        print_info("No optional packages selected, skipping...")
        if dry_run:
            sleep(2)
        
    return True