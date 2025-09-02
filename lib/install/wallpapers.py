# Utility functions
from includes import (
    print_header,
    print_info,
    confirm,
    Spinner,
)
from shared import (
    logger,
    log_heading,
    USER_WALLPAPERS_DIR,
    HYPRDOTS_WALLPAPERS_DIR
)

from time import sleep
import subprocess
import shutil
from pathlib import Path

def _apply_wallpaper() -> bool:
    """Apply wallpaper using waypaper."""
    try:
        subprocess.run(
            ["waypaper", "--restore"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logger.info("Wallpaper applied successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to apply wallpaper: {e}")
        return False

def _clone_repo(repo_url: str, clone_dir: Path) -> bool:
    """Clone a git repository into the given directory."""
    try:
        subprocess.run(
            ["git", "clone", repo_url, str(clone_dir)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logger.info("Cloned repository successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository: {e}")
        return False

def _install_wallpaper_collection() -> bool:
    """Clone wallpaper collection repo and copy image files only."""
    repo_url = "https://github.com/sbalghari/Wallpapers.git"
    clone_dir = Path("/tmp/wallpapers_collection")
    
    if clone_dir.exists():
        shutil.rmtree(clone_dir)
    clone_dir.mkdir(parents=True, exist_ok=True)
    
    if not _clone_repo(repo_url, clone_dir):
        return False

    try:
        USER_WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)
        for file in clone_dir.iterdir():
            if file.is_file() and file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
                shutil.copy2(file, USER_WALLPAPERS_DIR)
        logger.info("Wallpaper collection copied successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to copy wallpapers: {e}")
        return False

def install_wallpapers(dry_run: bool = False) -> bool:
    """Main installer function for wallpapers."""
    log_heading("Wallpapers installer started")
    print_header("Installing Wallpapers.")
    
    # Ask user up front for installing additional wallpaper collection
    install_collection = False if dry_run else confirm("Do you want to install my wallpapers collection?")
    
    with Spinner("Installing wallpapers...") as spinner:
        if dry_run:
            sleep(2)
            spinner.success("Dry run completed.")
            return True
        
        try:
            # Ensure base wallpapers dir exists
            USER_WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info("Ensured wallpapers dir exists.")
            
            # Copy default wallpapers
            spinner.update_text("Copying default wallpapers...")
            try:
                shutil.copytree(HYPRDOTS_WALLPAPERS_DIR, USER_WALLPAPERS_DIR, dirs_exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to copy default wallpapers: {e}")
                return False
            
            # Optionally install extra collection
            if install_collection:
                spinner.update_text("Installing wallpaper collection...")
                if not _install_wallpaper_collection():
                    spinner.error("Failed to install wallpaper collection.")
                    return False
                logger.info("User chose to install wallpaper collection.")
            else:
                logger.info("User chose not to install wallpaper collection.")
            
            # Apply wallpaper
            spinner.update_text("Applying wallpaper...")
            if not _apply_wallpaper():
                spinner.error("Failed to apply wallpaper.")
                return False
            
            spinner.success("Wallpapers installed successfully.")
            return True
        
        except Exception as e:
            logger.error(f"Wallpaper installation failed: {e}")
            spinner.error("Wallpaper installation failed.")
            return False
