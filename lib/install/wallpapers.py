# Utility functions
from includes import (
    print_header,
    Spinner,
)
from shared import (
    logger,
    log_heading,
    USER_WALLPAPERS_DIR,
    HYPRDOTS_WALLPAPERS_DIR 
    
)

from time import sleep
import shutil
import os

def install_wallpapers(dry_run: bool = False) -> bool:
    log_heading("Wallpapers installer started")
    print_header("Installing Wallpapers.")
    
    logger.info("Copying wallpapers...")
    with Spinner("Copying wallpapers...") as spinner:
        if dry_run:
            sleep(2)
        if not dry_run:
            logger.info("Creating wallpapers dir...")
            if not os.path.exists(USER_WALLPAPERS_DIR):
                os.makedirs(USER_WALLPAPERS_DIR, exist_ok=True)
                logger.info("Created wallpapers dir.")
            try:
                wallpapers = os.listdir(HYPRDOTS_WALLPAPERS_DIR)
                for i in wallpapers:
                    shutil.copy2(os.path.join(HYPRDOTS_WALLPAPERS_DIR, i), USER_WALLPAPERS_DIR)
                    logger.info("Wallpapers copied successfully")
            except Exception as e:
                logger.error(f"Failed to copy wallpapers: {e}")
                spinner.error("Failed to copy wallpapers.")
                return False
        spinner.success("Wallpapers copied successfully.")
        
    return True