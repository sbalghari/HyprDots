import subprocess

from includes.logger import logger

def apply_wallpaper() -> bool:
    """Apply wallpaper using waypaper."""
    try:
        subprocess.run(
            ["waypaper", "--restore"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info("Wallpaper applied successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to apply wallpaper: {e}")
        return False